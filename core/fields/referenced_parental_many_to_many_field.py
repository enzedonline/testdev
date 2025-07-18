# source: https://github.com/wagtail/wagtail/issues/9629#issuecomment-2004708133
# FIXME: Remove when this issue is fixed: https://github.com/wagtail/wagtail/issues/9629

from modelcluster.fields import ParentalManyToManyField


class ReferencedParentalManyToManyField(ParentalManyToManyField):
    def extract_references(self, value):
        # Yields tuples of (
        #     model, object_id, model_path, content_path,
        # )
        for item in value:
            yield (
                self.related_model, f'{item.pk}',
                'item',
                '',
            )