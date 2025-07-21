from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from PIL import Image, ImageDraw
from io import BytesIO
import base64

from .forms import DeviceModelForm, InsertForm
from .models import DeviceModel

from django.views.generic import FormView,CreateView,DetailView

class InsertCreate(FormView):

    form_class = InsertForm
    template_name = 'hotspot_insert_generator/insert.html'

    def form_valid(self, form):
        nwratio = 3
        qzone=10
        barcolor="#000"
        spccolor="#FFF"
        imgheight = 400
        final_imgwidth = 1400

        clean_data = form.cleaned_data

        barcode_data = clean_data["start_code"] + clean_data["barcode_number"] + clean_data["stop_code"]

        charpats={

            "0": {"pat":"0000011"}, 
            "1": {"pat":"0000110"},
            "2": {"pat":"0001001"},
            "3": {"pat":"1100000"},
            "4": {"pat":"0010010"},
            "5": {"pat":"1000010"},
            "6": {"pat":"0100001"},
            "7": {"pat":"0100100"},
            "8": {"pat":"0110000"},
            "9": {"pat":"1001000"},
            "A": {"pat":"0011010"},
            "B": {"pat":"0101001"},
            "C": {"pat":"0001011"},
            "D": {"pat":"0001110"},
            "-": {"pat":"0001100"},
            "$": {"pat":"0011000"},
            ":": {"pat":"1000101"},
            "/": {"pat":"1010001"},
            ".": {"pat":"1010100"},
            "+": {"pat":"0010101"},
        }

        narobar_width = 10

        numchars =len(barcode_data)

        img = Image.new("RGB", (int(final_imgwidth), imgheight),"#ffffff")

        # dry run to calculate width
        xpos = qzone * narobar_width
        for codepos in range(numchars):

            charpat = charpats[barcode_data[codepos]]["pat"]
            if charpat.count("1") == 2:
                xpos = xpos + 5 * narobar_width + 2 * narobar_width * nwratio
            else:
                xpos = xpos + 4 * narobar_width + 3 * narobar_width * nwratio
            xpos = xpos + narobar_width

        xpos = xpos - narobar_width
        xpos = xpos + qzone * narobar_width 


        img = Image.new("RGB", (xpos, imgheight),"#ffffff")

        img1 = ImageDraw.Draw(img)  

        xpos = qzone * narobar_width

        # full run to draw image
        for codepos in range(numchars):
            fillcolor=barcolor
            charpat = charpats[barcode_data[codepos]]["pat"]

            for charpos in range(len(charpat)):

                bandwidth = narobar_width if charpat[charpos] == "0" else narobar_width * nwratio
                shape = [(xpos, 10), (xpos + bandwidth, imgheight - 10)]
                img1.rectangle(shape, fill=fillcolor)
                xpos = xpos + bandwidth            
                fillcolor = spccolor if fillcolor==barcolor else barcolor
            xpos = xpos + narobar_width

        xpos = xpos - narobar_width
        xpos = xpos + qzone * narobar_width

        img = img.resize((int(xpos * (final_imgwidth / xpos)), imgheight))

        byio = BytesIO()
        img.save(byio, format="jpeg")
        data=byio.getvalue()

        codabar_image = base64.standard_b64encode(data).decode("utf-8")

        context_data = self.get_context_data()
        context_data["form"] = form
        context_data["codabar_image"] = codabar_image

        context_data["start_code"] = clean_data["start_code"]
        context_data["stop_code"] = clean_data["stop_code"]
        context_data["barcode_number"] = clean_data["barcode_number"]
        context_data["ssid"] = clean_data["ssid"]
        context_data["password"] = clean_data["password"]
        context_data["device_model"] = clean_data["device_model"]

        return render( self.request, self.template_name, context_data )

class DeviceModelCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'hotspot_insert_generator.add_devicemodel'
    model = DeviceModel
    form_class = DeviceModelForm
    template_name = "hotspot_insert_generator/devicemodel_form.html"

    def get_success_url(self):

        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": self.model._meta.app_label,
                    "model_name": self.model.__name__,
                },
            )
        return reverse_lazy("hotspot_insert_generator:device_detail", kwargs={"pk": self.object.pk})

class DeviceModelUpdate(PermissionRequiredMixin, CreateView):
    permission_required = 'hotspot_insert_generator.add_devicemodel'
    model = DeviceModel
    form_class = DeviceModelForm
    template_name = "hotspot_insert_generator/devicemodel_form.html"

    def get_success_url(self):
        return reverse_lazy("hotspot_insert_generator:device_detail", kwargs={"pk": self.object.pk})

class DeviceModelDetail(DetailView):
    model = DeviceModel
    template_name = "hotspot_insert_generator/devicemodel_detail.html"