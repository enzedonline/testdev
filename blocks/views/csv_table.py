from io import StringIO

import pandas as pd
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.views import View
from htmlmin import minify

def is_currency_column(column):
    # Ignore empty values
    non_empty_values = column.dropna().astype(str)
    # Regular expression pattern to match currency values
    currency_pattern = r'^\s*[+-]?\s*\$?\s*\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*$'
    # Check if all values in the column match the currency pattern
    is_currency = non_empty_values.str.match(currency_pattern).all()
    return is_currency

def render_html_table(table_block):
    try:
        if table_block["row_headers"]:
            df = pd.read_csv(
                StringIO(table_block["data"]),
                header="infer" if table_block["column_headers"] else None,
                index_col = 0
            )
        else:
            df = pd.read_csv(
                StringIO(table_block["data"]),
                header="infer" if table_block["column_headers"] else None
            )

        # Note: NaN is considered float by pandas 1.x, upgrade to >=2.2 to avoid this bug
        df = df.convert_dtypes()

        # set decimal places for float, set NA value representation as empty string
        dfs = df.style.format(precision=table_block["precision"], na_rep="")
        # hide column index row if no column headers
        if not table_block["column_headers"]:
            dfs = dfs.hide(axis=1, level=0)
        # hide row numbers (index) column if no row headers
        if not table_block["row_headers"]:
            dfs = dfs.hide(axis=0)

        # Align everything not an object (object=string) to the right
        right_align_columns = list(df.select_dtypes(exclude=["string", "object"]).columns)
        # right align currency strings
        for col in df.select_dtypes(["string", "object"]).columns:
            if is_currency_column(df[col]):
                right_align_columns.append(col)
        # create dataframe same dims as df, map css to relevant cells 
        classes = pd.DataFrame(index=df.index, columns=df.columns)
        classes[right_align_columns] = 'csv-table-right-align'
        dfs.set_td_classes(classes)

        # Add table classes and styles
        classes = "csv-table table table-striped table-hover"
        if table_block["compact"]: classes += " table-sm"
        if table_block["column_headers"]: classes += " csv-table-column-headers"
        if table_block["row_headers"]: classes += " csv-table-row-headers"
        dfs = dfs.set_table_attributes(f'class="{classes}"')

        # render table
        soup = BeautifulSoup(dfs.to_html(), "html.parser")
        thead = soup.find("thead")
        if table_block["column_headers"]:
            # align headers to match right aligned columns, add header divider to tbody
            if right_align_columns:
                # if column name repeated in table, it will right-align all matching column names
                # normally, pandas will suffix duplicate column names automatically
                for column in right_align_columns:
                    th_elements = thead.find_all("th", string=column)
                    for th_element in th_elements:
                        th_element["class"] = th_element.get("class", []) + ["csv-table-right-align"]
            tbody = soup.find("tbody")
            tbody["class"] = tbody.get("class", []) + ["table-group-divider"]
        else:
            # force no column headers - index label for row headers will render otherwise
            thead.extract()
        return str(soup)
    except Exception as e:
        raise e

class RenderCSVTableProxy(View):
    def post(self, request):
        try:
            data = request.POST
            table_block = {
                'data': data.get("data", ""),
                'precision': data.get("precision", 2),
                'column_headers': (data.get("column_headers", True)=='true'),
                'row_headers': (data.get("row_headers", False)=='true'),
                'compact': (data.get("compact", False)=='true')
            }
            # Process the data and generate minified HTML table
            html_table = render_html_table(table_block)
            return HttpResponse(minify(html_table.replace('\n','')).replace('> <', '><'))
        except Exception as e:
            # print(str(e))
            return HttpResponse(str(e), status=400)
        
