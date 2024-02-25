from django.http import FileResponse
import openpyxl
from openpyxl import Workbook

class ExportRecuExcelMixin:
   def get_attribute(self, obj, field):
       attr = getattr(obj, field)
       if hasattr(attr, '__str__'):
           # If the attribute is a model instance, use its __str__ method
           return str(attr)
       else:
           # Otherwise, just append the attribute value
           attr

   def export_as_excel(self, request, queryset):

       meta = self.model._meta
       field_names = ["Id",	"Nom client", "Phone client", "Email client", "Adresse Client",	"Famille", "Categorie",	"Objet",	"Marque",	"Probleme",	"Note",	"Prix",	"Accompte", "reste",	"status",	"Observation",	"Represantant",	"cree_a",	"modifie_a"]

       # Create a workbook and select the active worksheet
       wb = Workbook()
       ws = wb.active

       # Write headers
       ws.append(field_names)

       # Write data rows
       for obj in queryset:
           ws.append([
                getattr(obj, "id"),
                getattr(getattr(obj, "client"), "nom"),
                getattr(getattr(obj, "client"), "phone"),
                getattr(getattr(obj, "client"), "email"),
                getattr(getattr(obj, "client"), "adresse"),
                str(getattr(getattr(obj, "categorie"), "famille")),
                str(getattr(obj, "categorie")),
                str(getattr(obj, "objet")),
                getattr(obj, "marque"),
                getattr(obj, "probleme"),
                getattr(obj, "note"),
                getattr(obj, "prix"),
                getattr(obj, "accompte"),
                getattr(obj, "prix") - getattr(obj, "accompte"),
                str(getattr(obj, "status")),
                getattr(obj, "observation"),
                str(getattr(obj, "represantant")),
                getattr(obj, "cree_a"),
                getattr(obj, "modifie_a"),
           ])

       # Save the workbook to a file
       filename = f"{meta}.xlsx"
       wb.save(filename)

       # Create a response object with the contents of the file
       response = FileResponse(open(filename, 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
       response['Content-Disposition'] = f'attachment; filename={filename}'

       return response

   export_as_excel.short_description = "Exporter les Récus selectionné en XLSX"
