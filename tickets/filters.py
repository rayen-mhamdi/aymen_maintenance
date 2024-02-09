from django.contrib import admin


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((None, None),)
    

class IDFilter(InputFilter):
    title = 'ID' # Human-readable title which will be displayed in the admin sidebar
    parameter_name = 'id' # Parameter for the filter that will be used in the URL query

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        id_filter = self.value()
        if id_filter:
            return queryset.filter(id__exact=id_filter)
        else:
            return queryset