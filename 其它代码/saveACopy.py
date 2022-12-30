# coding=utf-8
import arcpy.mapping as mapping
mxd = mapping.MapDocument("C:/arcpyBook/Ch2/Crime_Ch2.mxd")
#mxd.title = "QQQ"
#print(mxd.title)
#layers = mapping.ListLayers(mxd)
#for df in mapping.ListDataFrames(mxd):
for lay in mapping.ListDataFrames(mxd):
    if lay.name == 'Crime':
        layers = mapping.ListLayers(mxd,'*in*',lay)
        for layer in layers:
           print(layer.name)
#for de in mapping.ListDataFrames(mxd):
    #print (de.name)