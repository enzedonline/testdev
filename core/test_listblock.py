from wagtail.rich_text import RichText
from blocks.collapsible_card import CollapsibleCard, CollapsibleCardBlock
from wagtail.blocks import ListBlock
from wagtail.blocks.list_block import ListValue
from wagtail.models import Page

pg=Page.objects.get(id=19).specific
lv=ListValue(ListBlock(CollapsibleCard))
lv.append({'header': 'Test 1', 'text': RichText('test1 text')})
lv.append({'header': 'Test 2', 'text': RichText('test2 text')})
pg.content.append(
    (
        (
            "collapsible_card_block",
            {
                "header_colour": 'bg-dark',
                "body_colour": 'bg-light',
                "cards": lv,
            },
        )
    )
)
pg.save()