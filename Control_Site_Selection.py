############################################
#Control
############################################

import arcpy
arcpy.env.workspace = "C:\Users\Administrator\Desktop\Bobafett\GridWatch\GridWatch.gdb\site_selection_testing"





##C1##
##C1. Similarly to the first step of the Control selection, SA of 300m is identified from all existing TX. The difference is in this case injection TX are included in the set of existing TX and are treated as existing TX. 


#Set local variables
#district = "NAME OF DISTRICT"
#LV_lines = "PATH TO LV LINES"
#Existing_TX = "PATH TO EXISTING TX LAYER"
#Injection_TX = "PATH TO INJECTION TX LAYER"
#Feeders = "PATH TO FEEDERS LAYER"
#network = "PATH TO NETWORK DATASET OF DISTRICT"
#distance_from_line = "25"
#district_siteID_range = 200
#control_point_count = int(arcpy.GetCount_management(Injection_TX).getOutput(0)) 
#Consider making count of injecitons


district = "Dansoman"
LV_lines = 'Exsititng__Lv'
Existing_TX = 'Existing_Transfomers'
Injection_TX = r'C:\Users\Administrator\Desktop\Bobafett\GridWatch\DANSOMAN\DANSOMAN\NEW_Trasnformers.shp'
Feeders = 'T11_KV_FEEDERS'
network = r'C:\Users\Administrator\Desktop\Bobafett\GridWatch\DANSOMAN\DANSOMAN\Dansoman_Grid.gdb\Dansoman_grid_components\Dansoman_grid_components_ND'
distance_from_line = "25"
district_siteID_range = 200
control_point_count = int(arcpy.GetCount_management(Injection_TX).getOutput(0)) 





####Scratch#####


#C1#
#existing and injection TX service area
Existing_TX_SA = arcpy.na.MakeServiceAreaLayer (network, "Existing_TX Service Area 300", "Length", "TRAVEL_FROM", "300" , "DETAILED_POLYS", "MERGE" , "DISKS", "NO_LINES" , "NON_OVERLAP", "NO_SPLIT", Feeders , "", "", "", "TRIM_POLYS", distance_from_line)
Existing_TX_SA = Existing_TX_SA.getOutput(0)

#Load Elements
arcpy.na.AddLocations (Existing_TX_SA, "Facilities", Existing_TX, "", "25 Meters")
arcpy.na.AddLocations (Existing_TX_SA, "Facilities", Injection_TX, "", "25 Meters")

#Solve
arcpy.na.Solve(Existing_TX_SA,"SKIP")

#CHECK FOR ERRORS

#Export polygon layer
Existing_TX_Polygons_300m = arcpy.SelectData_management (Existing_TX_SA, "Polygons")


#C2#
Existing_TX_SA_600m = arcpy.na.MakeServiceAreaLayer (network, "Existing_TX_SA_600m", "Length", "TRAVEL_FROM", "600" , "DETAILED_POLYS", "MERGE" , "DISKS", "NO_LINES" , "NON_OVERLAP", "NO_SPLIT", Feeders , "", "", "", "TRIM_POLYS", distance_from_line)
#Existing_TX_SA_600m = Existing_TX_Polygons_600m.getOutput(0)


#Load Elements
arcpy.na.AddLocations (Existing_TX_SA_600m, "Facilities", Injection_TX, "", "25 Meters")
arcpy.na.AddLocations (Existing_TX_SA_600m, "Facilities", Existing_TX, "", "25 Meters")

#Solve
arcpy.na.Solve(Existing_TX_SA_600m,"SKIP")

#CHECK FOR ERRORS

#Export polygon layer
Existing_TX_Polygons_600m = arcpy.SelectData_management (Existing_TX_SA_600m, "Polygons")




#C3#


#Erase 300m from 600m
Control_erased_poly = arcpy.Erase (Existing_TX_Polygons_600m, Existing_TX_Polygons_300m, "Control_Zone", "POLY", "0.00001")


#buffer 5m lv lines
arcpy.Buffer_analysis(LV_lines, "LV_lines_buffer5m", "5 Meters", "FULL", "ROUND", "ALL", )



#clip LV buffer with control buffer
arcpy.Clip_analysis('LV_lines_buffer5m', 'Control_Zone', "Control_Candidate_Zone")




#C4
#Generate random points 

arcpy.CreateRandom_Points_management("/control", "Control_Points", 'Control_Candidate_Zone', "", control_point_count, 300)



Control_SA = arcpy.na.MakeServiceAreaLayer (network, district+"_Control_SA", "Length", "TRAVEL_FROM", "200" , "DETAILED_POLYS", "NO_MERGE" , "DISKS", "NO_LINES" , "NON_OVERLAP", "NO_SPLIT", Feeders , "", "", "", "TRIM_POLYS", distance_from_line)
Control_SA = Control_SA.getOutput(0)



#C5
#Load Elements
arcpy.na.AddLocations (Control_SA, "Facilities", 'Control_Points', "", "25 Meters")
arcpy.na.AddLocations (Control_SA, "Polygon Barriers", Existing_TX_Polygons_300m, "", "25 Meters")

#Solve
arcpy.na.Solve(Control_SA,"SKIP")
#CHECK FOR ERRORS

#Save Injection transformers which were restricted by existing transformers
Control_restricted = arcpy.SelectData_management (Control_SA, "Facilities")
Control_restricted = arcpy.SelectLayerByAttribute_management (Control_restricted, "NEW_SELECTION",'"Status"= 3' )
arcpy.MakeFeatureLayer_management(Control_restricted,"Control_restricted")


#Calculate polycon areas
Control_Polygons = arcpy.SelectData_management (Control_SA, "Polygons")
Control_Polygons = Control_Polygons.getOutput(0)
Control_Polygons_withArea = arcpy.CalculateAreas_stats (Control_Polygons, "Control_Polygons")



#arcpy.MakeFeatureLayer_management(Control_Polygons_withArea,"Control_Polygons_Standard",'"F_AREA" >= 10000' )
arcpy.MakeFeatureLayer_management(Control_Polygons_withArea,"Control_Polygons_Small",'"F_AREA" <= 10000' )




if arcpy.management.GetCount('Control_Polygons_Small')[0] > "0":     
	Control_Points_Alt = arcpy.SelectLayerByLocation_management ('Control_Points', "INTERSECT", 'Control_Polygons_Small', "15 Meters")
	arcpy.MakeFeatureLayer_management(Control_Points_Alt,"Control_Points_Alt")
	#Injection_TX_Alt = Injection_TX_Alt.getOutput(0)
	Control_Alt_SA = arcpy.na.MakeServiceAreaLayer (network, district+"_Control_Alt_SA", "Length", "TRAVEL_FROM", "150" , "DETAILED_POLYS", "NO_MERGE" , "DISKS", "NO_LINES" , "NON_OVERLAP", "NO_SPLIT", Feeders , "", "", "", "TRIM_POLYS", distance_from_line)
	#Control_Alt_SA = Control_Alt_SA.getOutput(0)
	arcpy.na.AddLocations (Control_Alt_SA, "Facilities", Control_Points_Alt, "", "25 Meters")
	arcpy.na.AddLocations (Control_Alt_SA, "Facilities", Control_Points_restricted, "", "25 Meters")
	arcpy.na.Solve(Control_Alt_SA,"SKIP", "CONTINUE")
	#CHECK FOR ERRORS
	Control_Polygons_Alt = arcpy.SelectData_management (Control_SA, "Polygons")
	Control_Polygons_Alt = arcpy.MakeFeatureLayer_management(Control_Polygons_Alt, "Control_Polygons_Alt")
	#arcpy.SaveToLayerFile_management (Control_Polygons_Alt, "Control_Polygons_Alt")


else:
	Control_Polygons_Standard = arcpy.MakeFeatureLayer_management(Control_Polygons_withArea,"Control_Polygons_Standard",'"F_AREA" >= 10000' )


#T4#


#Collect and name all polygons
arcpy.Merge_management ([Control_Polygons_Standard, Control_Polygons_Alt], "Control_Sites")

##Visually Inspect Results. Check To Make Sure all requirements are met. If not, then create polygons of outliers mannually



#Create Lat/Lon Fields for polygon centroids

arcpy.AddGeometryAttributes_management('Control_Sites',"CENTROID")

#arcpy.AddField_management('Control_Sites',"Site_ID", "TEXT","" ,"",50,"","","","")
#arcpy.CalculateField_management('Control_Sites',"Site_ID", '!OBJECTID' + district_siteID_range, "PYTHON","")

