import arcpy.mapping as mapping
mxd = mapping.MapDocument('current')
mxd.activeDataFrame.zoomToselectedFeatures()
df = mapping.ListDataFrames(mxd,'Crime')[0]
