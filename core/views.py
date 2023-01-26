from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Employee
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.forms import DateTimeInput
import datetime
import logging
import pyodbc
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import azure.functions as func
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import psutil
import kaleido
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobClient
from azure.storage.blob import ContainerClient
import pandas as pd
import json
from io import BytesIO
import base64
from plotly.subplots import make_subplots
import plotly.io as pio
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.http import StreamingHttpResponse
class Index(LoginRequiredMixin, View):
    template = 'index.html'
    login_url = '/login/'
    
    def get(self, request):
        employees = Employee.objects.all()
        return render(request, self.template, {'employees': employees})


class Login(View):
    template = 'login.html'
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template, {'form': form})


@csrf_exempt
def about(request):

    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=sevendaypremium;AccountKey=YeFdLE5sLLsVceijHjRczp3GgZ70AtN4pHmTDlL73a98Om5SmWVL3WIA9xWo4hQ84u3FCirCqM3P+AStlvSSrQ==;EndpointSuffix=core.windows.net")
    container_clientGAS = blob_service_client.get_container_client("gasevents")
    container_clientCOAL = blob_service_client.get_container_client("coalevents")
    container_clientDUAL = blob_service_client.get_container_client("dualevents")
    container_clientWIND = blob_service_client.get_container_client("windevents")
    container_clientSOLAR = blob_service_client.get_container_client("solarevents")
    container_clientSTORAGE = blob_service_client.get_container_client("storageevents")
    container_clientOTHER = blob_service_client.get_container_client("otherevents")
    container_clientHYDRO = blob_service_client.get_container_client("hydroevents")



    
    eventlistGAS = []
    eventlistCOAL = []
    eventlistDUAL = []
    eventlistSTORAGE = []
    eventlistOTHER = []
    eventlistWIND = []
    eventlistHYDRO = []
    eventlistSOLAR = []


    blobs_listGAS = container_clientGAS.list_blobs()
    blobs_listCOAL = container_clientCOAL.list_blobs()
    blobs_listDUAL = container_clientDUAL.list_blobs()
    blobs_listHYDRO = container_clientHYDRO.list_blobs()
    blobs_listSOLAR = container_clientSOLAR.list_blobs()
    blobs_listWIND = container_clientWIND.list_blobs()
    blobs_listOTHER = container_clientOTHER.list_blobs()
    blobs_listSTORAGE = container_clientSTORAGE.list_blobs()

    
    for blob in blobs_listCOAL:
        blobs = blob.name
        eventlistCOAL.append(blobs)

    for blob in blobs_listGAS:
        blobs = blob.name
        eventlistGAS.append(blobs)


    for blob in blobs_listDUAL:
        blobs = blob.name
        eventlistDUAL.append(blobs)

    for blob in blobs_listHYDRO:
        blobs = blob.name
        eventlistHYDRO.append(blobs)


    for blob in blobs_listSOLAR:
        blobs = blob.name
        eventlistSOLAR.append(blobs)

    for blob in blobs_listWIND:
        blobs = blob.name
        eventlistWIND.append(blobs)


    for blob in blobs_listOTHER:
        blobs = blob.name
        eventlistOTHER.append(blobs)

    for blob in blobs_listSTORAGE:
        blobs = blob.name
        eventlistSTORAGE.append(blobs)

    
    arrGAS = []
    arrDual = []
    arrSolar = []
    arrCoal = []
    arrHydro = []
    arrWind = []
    arrStorage = []
    arrOther = []


    

    for i in range(0,len(list(eventlistSTORAGE))):
        blob_client = container_clientSTORAGE.get_blob_client(eventlistSTORAGE[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistSTORAGE[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrStorage.append(json_records)
        contextStorage = {'Storage': arrStorage}

    for i in range(0,len(list(eventlistOTHER))):
        blob_client = container_clientOTHER.get_blob_client(eventlistOTHER[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistOTHER[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrOther.append(json_records)
        contextStorage = {'d': arrOther}


    for i in range(0,len(list(eventlistGAS))):
        blob_client = container_clientGAS.get_blob_client(eventlistGAS[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistGAS[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrGAS.append(json_records)
        contextGas = {'d': arrGAS}

    for i in range(0,len(list(eventlistDUAL))):
        blob_client = container_clientDUAL.get_blob_client(eventlistDUAL[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistDUAL[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrDual.append(json_records)
        contextDual = {'d': arrDual}


    for i in range(0,len(list(eventlistCOAL))):
        blob_client = container_clientCOAL.get_blob_client(eventlistCOAL[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistCOAL[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrCoal.append(json_records)
        contextCOAL = {'d': arrCoal}




    for i in range(0,len(list(eventlistHYDRO))):
        blob_client = container_clientHYDRO.get_blob_client(eventlistHYDRO[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistHYDRO[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrHydro.append(json_records)
        contextHydro = {'d': arrHydro}



    for i in range(0,len(list(eventlistWIND))):
        blob_client = container_clientWIND.get_blob_client(eventlistWIND[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistWIND[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrWind.append(json_records)
        contextWind = {'d': arrWind}


    for i in range(0,len(list(eventlistSOLAR))):
        blob_client = container_clientSOLAR.get_blob_client(eventlistSOLAR[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistSOLAR[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrSolar.append(json_records)
        contextSolar = {'d': arrSolar}

    
    gas = []
    coal = []
    dual  = []
    hydro  = []
    wind  = []
    solar  = []
    storage  = []
    other  = []
    ###################################################################################################

    container_clientGAS90 = blob_service_client.get_container_client("90gasevent")
    container_clientCOAL90 = blob_service_client.get_container_client("90coalevent")
    container_clientDUAL90 = blob_service_client.get_container_client("90dualevent")
    container_clientWIND90 = blob_service_client.get_container_client("90windevent")
    container_clientSOLAR90 = blob_service_client.get_container_client("90solarevent")
    container_clientSTORAGE90 = blob_service_client.get_container_client("90storageevent")
    container_clientOTHER90 = blob_service_client.get_container_client("90otherevent")
    container_clientHYDRO90 = blob_service_client.get_container_client("90hydroevent")

    eventlistGAS90 = []
    eventlistCOAL90 = []
    eventlistDUAL90 = []
    eventlistSTORAGE90 = []
    eventlistOTHER90 = []
    eventlistWIND90 = []
    eventlistHYDRO90 = []
    eventlistSOLAR90 = []

    blobs_listGAS90 = container_clientGAS90.list_blobs()
    blobs_listCOAL90 = container_clientCOAL90.list_blobs()
    blobs_listDUAL90 = container_clientDUAL90.list_blobs()
    blobs_listHYDRO90 = container_clientHYDRO90.list_blobs()
    blobs_listSOLAR90 = container_clientSOLAR90.list_blobs()
    blobs_listWIND90 = container_clientWIND90.list_blobs()
    blobs_listOTHER90 = container_clientOTHER90.list_blobs()
    blobs_listSTORAGE90 = container_clientSTORAGE90.list_blobs()


    for blob in blobs_listCOAL90:
        blobs = blob.name
        eventlistCOAL90.append(blobs)

    for blob in blobs_listGAS90:
        blobs = blob.name
        eventlistGAS90.append(blobs)


    for blob in blobs_listDUAL90:
        blobs = blob.name
        eventlistDUAL90.append(blobs)

    for blob in blobs_listHYDRO90:
        blobs = blob.name
        eventlistHYDRO90.append(blobs)


    for blob in blobs_listSOLAR90:
        blobs = blob.name
        eventlistSOLAR90.append(blobs)

    for blob in blobs_listWIND90:
        blobs = blob.name
        eventlistWIND90.append(blobs)


    for blob in blobs_listOTHER90:
        blobs = blob.name
        eventlistOTHER90.append(blobs)

    for blob in blobs_listSTORAGE90:
        blobs = blob.name
        eventlistSTORAGE90.append(blobs)

    arrGAS90 = []
    arrDual90 = []
    arrSolar90 = []
    arrCoal90 = []
    arrHydro90 = []
    arrWind90 = []
    arrStorage90 = []
    arrOther90 = []


    

    for i in range(0,len(list(eventlistSTORAGE90))):
        blob_client = container_clientSTORAGE90.get_blob_client(eventlistSTORAGE90[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistSTORAGE90[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrStorage90.append(json_records)
        contextStorage = {'Storage': arrStorage}

    for i in range(0,len(list(eventlistOTHER90))):
        blob_client = container_clientOTHER90.get_blob_client(eventlistOTHER90[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistOTHER90[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrOther90.append(json_records)
        contextStorage = {'d': arrOther}


    for i in range(0,len(list(eventlistGAS90))):
        blob_client = container_clientGAS90.get_blob_client(eventlistGAS90[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistGAS90[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrGAS90.append(json_records)
        contextGas = {'d': arrGAS}

    for i in range(0,len(list(eventlistDUAL90))):
        blob_client = container_clientDUAL90.get_blob_client(eventlistDUAL90[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistDUAL90[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrDual90.append(json_records)
        contextDual = {'d': arrDual}


    for i in range(0,len(list(eventlistCOAL90))):
        blob_client = container_clientCOAL90.get_blob_client(eventlistCOAL90[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistCOAL90[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrCoal90.append(json_records)
        contextCOAL = {'d': arrCoal}




    for i in range(0,len(list(eventlistHYDRO90))):
        blob_client = container_clientHYDRO90.get_blob_client(eventlistHYDRO90[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistHYDRO90[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrHydro90.append(json_records)
        contextHydro = {'d': arrHydro}



    for i in range(0,len(list(eventlistWIND90))):
        blob_client = container_clientWIND90.get_blob_client(eventlistWIND90[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistWIND90[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrWind90.append(json_records)
        contextWind = {'d': arrWind}


    for i in range(0,len(list(eventlistSOLAR90))):
        blob_client = container_clientSOLAR90.get_blob_client(eventlistSOLAR90[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistSOLAR90[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrSolar90.append(json_records)
        contextSolar = {'d': arrSolar}

    gas90 = []
    coal90 = []
    dual90  = []
    hydro90  = []
    wind90  = []
    solar90  = []
    storage90  = []
    other90  = []
    #################################################################################################




    container_clientGASMONTH = blob_service_client.get_container_client("monthlygasevent")
    container_clientCOALMONTH = blob_service_client.get_container_client("monthlycoalevent")
    container_clientDUALMONTH = blob_service_client.get_container_client("monthlydualevent")
    container_clientWINDMONTH = blob_service_client.get_container_client("monthlywindevent")
    container_clientSOLARMONTH = blob_service_client.get_container_client("monthlysolarevent")
    container_clientSTORAGEMONTH = blob_service_client.get_container_client("monthlystorageevent")
    container_clientOTHERMONTH = blob_service_client.get_container_client("monthlyotherevent")
    container_clientHYDROMONTH = blob_service_client.get_container_client("monthlyhydroevent")

    eventlistGASMONTHLY = []
    eventlistCOALMONTHLY = []
    eventlistDUALMONTHLY = []
    eventlistSTORAGEMONTHLY = []
    eventlistOTHERMONTHLY = []
    eventlistWINDMONTHLY = []
    eventlistHYDROMONTHLY = []
    eventlistSOLARMONTHLY = []

    blobs_listGASMONTHLY = container_clientGASMONTH.list_blobs()
    blobs_listCOALMONTHLY = container_clientCOALMONTH.list_blobs()
    blobs_listDUALMONTHLY = container_clientDUALMONTH.list_blobs()
    blobs_listHYDROMONTHLY = container_clientHYDROMONTH.list_blobs()
    blobs_listSOLARMONTHLY = container_clientSOLARMONTH.list_blobs()
    blobs_listWINDMONTHLY = container_clientWINDMONTH.list_blobs()
    blobs_listOTHERMONTHLY = container_clientOTHERMONTH.list_blobs()
    blobs_listSTORAGEMONTHLY = container_clientSTORAGEMONTH.list_blobs()

    
    for blob in blobs_listCOALMONTHLY:
        blobs = blob.name
        eventlistCOALMONTHLY.append(blobs)

    for blob in blobs_listGASMONTHLY:
        blobs = blob.name
        eventlistGASMONTHLY.append(blobs)


    for blob in blobs_listDUALMONTHLY:
        blobs = blob.name
        eventlistDUALMONTHLY.append(blobs)

    for blob in blobs_listHYDROMONTHLY:
        blobs = blob.name
        eventlistHYDROMONTHLY.append(blobs)


    for blob in blobs_listSOLARMONTHLY:
        blobs = blob.name
        eventlistSOLARMONTHLY.append(blobs)

    for blob in blobs_listWINDMONTHLY:
        blobs = blob.name
        eventlistWINDMONTHLY.append(blobs)


    for blob in blobs_listOTHERMONTHLY:
        blobs = blob.name
        eventlistOTHERMONTHLY.append(blobs)

    for blob in blobs_listSTORAGEMONTHLY:
        blobs = blob.name
        eventlistSTORAGEMONTHLY.append(blobs)

    arrGASMONTH = []
    arrDualMONTH = []
    arrSolarMONTH = []
    arrCoalMONTH = []
    arrHydroMONTH = []
    arrWindMONTH = []
    arrStorageMONTH = []
    arrOtherMONTH = []

    for i in range(0,len(list(eventlistSTORAGEMONTHLY))):
        blob_client = container_clientSTORAGEMONTH.get_blob_client(eventlistSTORAGEMONTHLY[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistSTORAGEMONTHLY[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrStorageMONTH.append(json_records)
        contextStorage = {'Storage': arrStorage}

    for i in range(0,len(list(eventlistOTHERMONTHLY))):
        blob_client = container_clientOTHER90.get_blob_client(eventlistOTHERMONTHLY[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistOTHERMONTHLY[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrOtherMONTH.append(json_records)
        contextStorage = {'d': arrOther}


    for i in range(0,len(list(eventlistGASMONTHLY))):
        blob_client = container_clientGAS.get_blob_client(eventlistGASMONTHLY[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistGASMONTHLY[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrGASMONTH.append(json_records)
        contextGas = {'d': arrGAS}

    for i in range(0,len(list(eventlistDUALMONTHLY))):
        blob_client = container_clientDUALMONTH.get_blob_client(eventlistDUALMONTHLY[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistDUALMONTHLY[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrDualMONTH.append(json_records)
        contextDual = {'d': arrDual}


    for i in range(0,len(list(eventlistCOALMONTHLY))):
        blob_client = container_clientCOALMONTH.get_blob_client(eventlistCOALMONTHLY[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistCOALMONTHLY[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrCoalMONTH.append(json_records)
        contextCOAL = {'d': arrCoal}




    for i in range(0,len(list(eventlistHYDROMONTHLY))):
        blob_client = container_clientHYDROMONTH.get_blob_client(eventlistHYDROMONTHLY[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistHYDROMONTHLY[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrHydroMONTH.append(json_records)
        contextHydro = {'d': arrHydro}



    for i in range(0,len(list(eventlistWINDMONTHLY))):
        blob_client = container_clientWINDMONTH.get_blob_client(eventlistWINDMONTHLY[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistWINDMONTHLY[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrWindMONTH.append(json_records)
        contextWind = {'d': arrWind}


    for i in range(0,len(list(eventlistSOLARMONTHLY))):
        blob_client = container_clientSOLARMONTH.get_blob_client(eventlistSOLARMONTHLY[i])
        df = blob_client.download_blob()
        df = pd.read_csv(df)
        df['blobname'] = eventlistSOLARMONTHLY[i]
        json_records = df.reset_index().to_json(orient ='records')

        json_records = json.loads(json_records)
        arrSolarMONTH.append(json_records)
        contextSolar = {'d': arrSolar}

    gasMONTH = []
    coalMONTH = []
    dualMONTH  = []
    hydroMONTH  = []
    windMONTH  = []
    solarMONTH  = []
    storageMONTH  = []
    otherMONTH  = []
    #################################################################################################
    if request.method == 'POST':
        gas = request.POST.getlist('gas')
        print(gas)
        if len(gas) > 0:
            for i in range(len(gas)):
                container_clientGAS.delete_blob(blob=gas[i])
        gas90 = request.POST.getlist('gas90')
        print(gas90)
        if len(gas90) > 0:
            for i in range(len(gas90)):
                container_clientGAS90.delete_blob(blob=gas90[i])
        gasMONTH = request.POST.getlist('gasMONTH')
        print(gasMONTH)
        if len(gasMONTH) > 0:
            for i in range(len(gasMONTH)):
                container_clientGASMONTH.delete_blob(blob=gasMONTH[i])


####################################################################################################
        hydro = request.POST.getlist('hydro')
        print(hydro)
        if len(hydro) > 0:
            for i in range(len(hydro)):
                container_clientHYDRO.delete_blob(blob=hydro[i])
        hydro90 = request.POST.getlist('hydro90')
        print(hydro90)
        if len(hydro90) > 0:
            for i in range(len(hydro90)):
                container_clientHYDRO90.delete_blob(blob=hydro90[i])
        hydroMONTH = request.POST.getlist('hydroMONTH')
        print(hydroMONTH)
        if len(hydroMONTH) > 0:
            for i in range(len(hydroMONTH)):
                container_clientHYDROMONTH.delete_blob(blob=hydroMONTH[i])
####################################################################################################        
        storage = request.POST.getlist('storage')
        print(storage)
        if len(storage) > 0:
            for i in range(len(storage)):
                container_clientSTORAGE.delete_blob(blob=storage[i])
        storage90 = request.POST.getlist('storage90')
        print(storage90)
        if len(storage90) > 0:
            for i in range(len(storage90)):
                container_clientSTORAGE90.delete_blob(blob=storage90[i])
        storageMONTH = request.POST.getlist('storageMONTH')
        if len(storageMONTH) > 0:
            for i in range(len(storageMONTH)):
                container_clientSTORAGEMONTH.delete_blob(blob=storageMONTH[i])
####################################################################################################        
        other = request.POST.getlist('other')
        print(other)
        if len(other) > 0:
            for i in range(len(other)):
                container_clientOTHER.delete_blob(blob=other[i])
        other90 = request.POST.getlist('other90')
        print(other90)
        if len(other90) > 0:
            for i in range(len(other90)):
                container_clientOTHER90.delete_blob(blob=other90[i])
        otherMONTH = request.POST.getlist('otherMONTH')
        if len(otherMONTH) > 0:
            for i in range(len(otherMONTH)):
                container_clientOTHERMONTH.delete_blob(blob=otherMONTH[i])
####################################################################################################        
        solar = request.POST.getlist('solar')
        print(solar)
        if len(solar) > 0:
            for i in range(len(solar)):
                container_clientSOLAR.delete_blob(blob=solar[i])
        solar90 = request.POST.getlist('solar90')
        print(solar90)
        if len(solar90) > 0:
            for i in range(len(solar90)):
                container_clientSOLAR90.delete_blob(blob=solar90[i])
        solarMONTH = request.POST.getlist('solarMONTH')
        if len(solarMONTH) > 0:
            for i in range(len(solarMONTH)):
                container_clientSOLARMONTH.delete_blob(blob=solarMONTH[i])
####################################################################################################        
        dual = request.POST.getlist('dual')
        print(dual)
        if len(dual) > 0:
            for i in range(len(dual)):
                container_clientDUAL.delete_blob(blob=dual[i])
        dual90 = request.POST.getlist('dual90')
        print(dual90)
        if len(dual90) > 0:
            for i in range(len(dual90)):
                container_clientDUAL90.delete_blob(blob=dual90[i])
        dualMONTH = request.POST.getlist('dualMONTH')
        print(dualMONTH)
        if len(dualMONTH) > 0:
            for i in range(len(dualMONTH)):
                container_clientDUALMONTH.delete_blob(blob=dualMONTH[i])
####################################################################################################        
        coal = request.POST.getlist('coal')
        print(coal)
        if len(coal) > 0:
            for i in range(len(coal)):
                container_clientCOAL.delete_blob(blob=coal[i])
        coal90 = request.POST.getlist('coal90')
        print(coal90)
        if len(coal90) > 0:
            for i in range(len(coal90)):
                container_clientCOAL90.delete_blob(blob=coal90[i])
        coalMONTH = request.POST.getlist('coalMONTH')
        print(coalMONTH)
        if len(coalMONTH) > 0:
            for i in range(len(coalMONTH)):
                container_clientCOALMONTH.delete_blob(blob=coalMONTH[i])
####################################################################################################        
        wind = request.POST.getlist('wind')
        print(wind)
        if len(wind) > 0:
            for i in range(len(wind)):
                container_clientWIND.delete_blob(blob=wind[i])
        wind90 = request.POST.getlist('wind90')
        print(wind90)
        if len(wind90) > 0:
            for i in range(len(wind90)):
                container_clientWIND90.delete_blob(blob=wind90[i])    
        windMONTH = request.POST.getlist('windMONTH')
        print(windMONTH)
        if len(windMONTH) > 0:
            for i in range(len(windMONTH)):
                container_clientWINDMONTH.delete_blob(blob=windMONTH[i])        
        
        
        LENGTHD = len(wind) + len(coal) + len(dual) + len(solar) + len(storage) + len(other) + len(coal) + len(gas)
        LENGTH90 = len(wind90) + len(coal90) + len(dual90) + len(solar90) + len(storage90) + len(other90) + len(coal90) + len(gas90)
        LENGTHMONTH = len(windMONTH) + len(coalMONTH) + len(dualMONTH) + len(solarMONTH) + len(storageMONTH) + len(otherMONTH) + len(coalMONTH) + len(gasMONTH)
        if LENGTHD + LENGTH90 + LENGTHMONTH > 0:
             return redirect('index.html')
    return render(request,'index.html',{'gas':arrGAS,'hydro':arrHydro,'solar':arrSolar,
    'wind':arrWind,'coal':arrCoal,'dual':arrDual,'storage':arrStorage,
    'other':arrOther,
    
    'gas90':arrGAS90,'coal90':arrCoal90,'dual90':arrDual90,'hydro90':arrHydro90,'storage90':arrStorage90,'other90':arrOther90,'wind90':arrWind90,'solar90':arrSolar90,
    
    'gasMONTH':arrGASMONTH,'coalMONTH':arrCoalMONTH,'dualMONTH':arrDualMONTH,'hydroMONTH':arrHydroMONTH,'storage90':arrStorage90,'other90':arrOther90,'wind90':arrWind90,'solar90':arrSolar90,})





# @csrf_exempt
# def stream(request):
#     import time
#     import datetime
#     def event_stream():
#         while True:
#             time.sleep(3)
#             yield 'data: The server time is: %s\n\n' % datetime.datetime.now()
#     return StreamingHttpResponse(event_stream(), content_type='text/event-stream')



# @csrf_exempt
# def stream(request):
#     import time
#     import datetime
#     blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=sevendaypremium;AccountKey=YeFdLE5sLLsVceijHjRczp3GgZ70AtN4pHmTDlL73a98Om5SmWVL3WIA9xWo4hQ84u3FCirCqM3P+AStlvSSrQ==;EndpointSuffix=core.windows.net")
#     container_clientGAS = blob_service_client.get_container_client("gasevents")
#     eventlistGAS = []
#     blobs_listGAS = container_clientGAS.list_blobs()
#     def event_stream():
#         while True:
#             time.sleep(3)
#             blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=sevendaypremium;AccountKey=YeFdLE5sLLsVceijHjRczp3GgZ70AtN4pHmTDlL73a98Om5SmWVL3WIA9xWo4hQ84u3FCirCqM3P+AStlvSSrQ==;EndpointSuffix=core.windows.net")
#             container_clientGAS = blob_service_client.get_container_client("90gasevent")
#             eventlistGAS = []
#             blobs_listGAS = container_clientGAS.list_blobs()
            
#             for blob in blobs_listGAS:
#                 blobs = blob.name
#                 eventlistGAS.append(blobs)
            
#             arrGAS=[]
            
#             for i in range(0,len(list(eventlistGAS))):
#                 blob_client = container_clientGAS.get_blob_client(eventlistGAS[i])
#                 df = blob_client.download_blob()
#                 df = pd.read_csv(df)
#                 df['blobname'] = eventlistGAS[i]
#                 json_records = df.reset_index().to_json(orient ='records')

#                 json_records = json.loads(json_records)
#                 arrGAS.append(json_records)
#                 contextGas = {'d': arrGAS}
            
#             yield 'data: The server time is: %s\n\n' % contextGas
#     return StreamingHttpResponse(event_stream(), content_type='text/event-stream')




# from django.shortcuts import render
# from django.http import HttpResponse
# import requests
# # Create your views here.
# def users(request):
#     #pull data from third party rest api
#     response = requests.get('https://jsonplaceholder.typicode.com/users')
#     #convert reponse data into json
#     users = response.json()
#     #print(users)
#     return render(request, "users.html", {'users': users})
#     pass


@csrf_exempt
def charts(request,vuv=None):


    def init_connection():
        
        server =r'tcp:supowerdatabase.database.windows.net' 
        database =r'SUpowerFinancials' 
        username =r'micoconnell1' 
        password =r'anisoTropical+308'
        driver= r'{ODBC Driver 17 for SQL Server}'
        
        cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' +
        server + ';PORT=1433;DATABASE=' + database +
        ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()
        return cursor

    cursor = init_connection()


    result = cursor.execute("SELECT * FROM dbo.OpenInterestProd WHERE DateModified > '2022-12-01' ORDER BY DateModified DESC ")
    rows = result.fetchall()
    cols = []
    #result = cursor.execute('SELECT * FROM dbo.AILForecasts ORDER BY dateModified DESC')

    for i,_ in enumerate(result.description):
        cols.append(result.description[i][0])
        

    df = pd.DataFrame(np.array(rows), columns=cols)



    def openTracker(df,temp=0):
        df=df
        temp=temp
        if temp == 0:

            temp=temp
            
            print(temp)
            df=df
            def yesterday(frmt='%Y-%m-%d', string=True):
                
                yesterday = datetime.now() - timedelta(0)
                if string:
                    return yesterday.strftime(frmt)
                return yesterday

            frmt='%Y-%m-%d'
            currentMonth = datetime.today().replace(day=1)
            currentMonth=currentMonth.strftime(frmt)

            def daybefore(frmt='%Y-%m-%d', string=True):
                
                yesterday = datetime.now() - timedelta(1)
                if string:
                    return yesterday.strftime(frmt)
                return yesterday

            def dateFilter(frmt='%Y-%m-%d', string=True):
                
                yesterday = datetime.now() + timedelta(1000)
                if string:
                    return yesterday.strftime(frmt)
                return yesterday

            yesterday=yesterday()
            daybefore=daybefore()
            dateFilter=dateFilter()
        else:
            
            temp=temp
            temp=temp[0]
            format='%Y-%m-%d'
            temp=datetime.strptime(temp, format)
            print(temp)
            df=df
            def yesterday(temp,frmt='%Y-%m-%d', string=True):
                temp=temp
                yesterday = temp - timedelta(0)
                if string:
                    return yesterday.strftime(frmt)
                return yesterday

            frmt='%Y-%m-%d'
            currentMonth = temp.replace(day=1)
            currentMonth=currentMonth.strftime(frmt)

            def daybefore(temp,frmt='%Y-%m-%d', string=True):
                temp=temp
                yesterday = temp - timedelta(1)
                if string:
                    return yesterday.strftime(frmt)
                return yesterday

            def dateFilter(temp,frmt='%Y-%m-%d', string=True):
                temp=temp
                yesterday = temp + timedelta(1000)
                if string:
                    return yesterday.strftime(frmt)
                return yesterday

            yesterday=yesterday(temp)
            daybefore=daybefore(temp)
            dateFilter=dateFilter(temp)
        df['BeginDate'] =  pd.to_datetime(df['BeginDate'])
        df['EndDate'] =  pd.to_datetime(df['EndDate'])
        df['DateModified'] =  pd.to_datetime(df['DateModified'])
        df['timeElasped'] = df['EndDate'] - df['BeginDate']
        df['timeElasped'] = df['timeElasped'] + np.timedelta64(1, 'D')
        df['timeElasped'] = (df['timeElasped'].values.astype(float)) / 86400000000000
        df['netOI'] = df['netOI'].replace(',','', regex=True)
        df['netOIMW'] = (df['netOI'].values.astype(float))
        df = df[df['timeElasped'] > 27 ]
        df['netOIMW'] = df['netOIMW'] / (df['timeElasped'] * 24)

        df_yesterday = df[df['DateModified'] == yesterday]
        df_daybefore = df[df['DateModified'] == daybefore]

        #df_daybefore = df_daybefore[df_daybefore['DateModified'] == yesterday]


        df_yesterday = df_yesterday.drop_duplicates()
        df_daybefore = df_daybefore.drop_duplicates()
        df_daybefore['netOIMW']= pd.to_numeric(df_daybefore['netOIMW'])
        df_daybefore= df_daybefore.set_index('BeginDate')

        df_yesterday['netOIMW']= pd.to_numeric(df_yesterday['netOIMW'])
        df_yesterday= df_yesterday.set_index('BeginDate')

        df_yesterdayseries = df_yesterday['netOIMW']
        df_daybeforeseries = df_daybefore['netOIMW']
        differences = df_yesterdayseries - df_daybeforeseries
        differences = differences.reset_index()
        #df_yesterday= df_yesterday.set_index('BeginDate')



        differences['BeginDate'] = pd.to_datetime(differences['BeginDate'])
        differences= differences.set_index('BeginDate')
        df_yesterday = df_yesterday[df_yesterday.index < dateFilter]
        differences = differences[differences.index < dateFilter]



        df_yesterday = df_yesterday[df_yesterday.index >= currentMonth]
        differences = differences[differences.index >= currentMonth]


        #differences = differences.drop_duplicates()
        differences= differences.dropna()

        differences["Color"] = np.where(differences["netOIMW"]<0, 'red', 'blue')
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Bar(x=differences.index, y=differences.netOIMW,marker_color=differences.Color, name=" New Open Interest (MW)", text=differences.netOIMW),
            secondary_y=True,
        )
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        fig.add_trace(
            go.Scatter(x=df_yesterday.index, y=df_yesterday.netOIMW, name="Total Open Interest (MW)"),
            secondary_y=False,
        )

        fig.update_layout(yaxis_range=[0,2000])
        fig.update_layout(yaxis2_range=[-50,200])

        fig.update_yaxes(title_text="<b>Net Open Interest</b>", secondary_y=False)
        fig.update_yaxes(title_text="<b>Net Change (MW)</b>", secondary_y=True)
        fig.update_xaxes(title_text="Date (Month)")
        fig.update_layout(
        autosize=True,
        width=1500,
        height=600,

        )

        graph = fig.to_html(full_html=False, default_height=500, default_width=700)
        context = {'graph': graph}
        return context

    

    


    if request.POST:
        temp = request.POST.getlist('bday')
        context = openTracker(df,temp)
        return render(request, "charts.html", context)
    context=openTracker(df,0)
    return render(request, "charts.html", context)
    
    



# Create your views .
@csrf_exempt
def home(request):
    if request.method == 'POST':
        print("as")
    

    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=openinteresthtml;AccountKey=CXyBp2UtmutNqVF07OAPJanuEF2hC//0oIbLQX5Npzxr/BnL0utnnEa+A/BW9U/7oigKWe/gyTAq+ASt6r1Zmw==;EndpointSuffix=core.windows.net")
    container_clientGAS = blob_service_client.get_container_client("historical")
    blob_client = container_clientGAS.get_blob_client('master.html')
    df = blob_client.download_blob()

    return render(request,"home.html")  
from azure.servicebus import ServiceBusClient
from forms import ServiceBusForm


def service_bus_view(request):
    if request.method == 'POST':
        form = ServiceBusForm(request.POST)
        if form.is_valid():
            conn_str = form.cleaned_data['conn_str']
            sb_client = ServiceBusClient.from_connection_string(conn_str)
            # do something with the service bus client
            return render(request, 'dashboard.html', {'form': form})
    else:
        form = ServiceBusForm()
    return render(request, 'service_bus_form.html', {'form': form})