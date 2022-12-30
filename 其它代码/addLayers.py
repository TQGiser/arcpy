import arcpy.mapping as mapping
mxd = mapping.MapDocument("current")
df = mapping.ListDataFrames(mxd)[0]
layer = (r"c:/ArcpyBook/data/School_Districts.lyr")
mapping.AddLayer(df,layer,'AUTO_ARRANGE')


import arcpy.mapping as mapping
mxd = mapping.MapDocument("CURRENT")
df = mapping.ListDataFrames(mxd)[0]
layer = mapping.Layer(r"C:\ArcpyBook\data\School_Districts.lyr")
mapping.AddLayer(df,layer,"AUTO_ARRANGE")
