############################################
#Treatment
############################################



import arcpy

##T1##
#SA of 300m was identified from existing TX, given they do not reach injection TX. If they reach an injection TX, the SA stops.


#Set local variables
district = "NAME OF DISTRICT"
LV_lines = "PATH TO LV LINES"
Existing_TX = "PATH TO EXISTING TX LAYER"
Injection_TX = "PATH TO INJECTION TX LAYER"
Feeders = "PATH TO FEEDERS LAYER"
network = "PATH TO NETWORK DATASET OF DISTRICT"
distance_from_line = "25"
district_siteID_range = 200


#existing TX service area
Existing_TX_SA = arcpy.na.MakeServiceAreaLayer (network, "Existing_TX Service Area", "Length", "TRAVEL_FROM", "300" , "DETAILED_POLYS", "MERGE" , "DISKS", "NO_LINES" , "NON_OVERLAP", "NO_SPLIT", Feeders , "", "", "", "TRIM_POLYS", distance_from_line)
Existing_TX_SA = Existing_TX_SA.getOutput(0)

#Load Elements
arcpy.na.AddLocations (Existing_TX_SA, "Facilities", Existing_TX, "field mapping", "25 Meters")
arcpy.na.AddLocations (Existing_TX_SA, "Point Barriers", Injection_TX, "field mapping", "25 Meters")

#Solve
arcpy.na.Solve(Existing_TX_SA,"SKIP")
#CHECK FOR ERRORS

#Export polygon layer
Existing_TX_Polygons = arcpy.SelectData_management (Existing_TX_SA, "Polygons")


##T2##
#SA of 200m was drawn from the injection TX sites. 
#Setting existing TX SA as a barrier prevents the SA made in the previous step from being crossed or considered as a valid injection TX SA. 
#This method allows to include LV lines that extend from the injection TX, are terminal, 
#and can be most directly attributed to the injection TX to be prioritized as treatment sites.

Treatment_SA = arcpy.na.MakeServiceAreaLayer (network, district+"_Treatment_SA", "Length", "TRAVEL_FROM", "200" , "DETAILED_POLYS", "NO_MERGE" , "DISKS", "NO_LINES" , "NON_OVERLAP", "NO_SPLIT", Feeders , "", "", "", "TRIM_POLYS", distance_from_line)
Treatment_SA = Treatment_SA.getOutput(0)


#Load Elements
arcpy.na.AddLocations (Treatment_SA, "Facilities", Injection_TX, "", "25 Meters")
arcpy.na.AddLocations (Treatment_SA, "Polygon Barriers", Existing_TX_Polygons, "", "25 Meters")

#Solve
arcpy.na.Solve(Treatment_SA,"SKIP")
#CHECK FOR ERRORS

#Save Injection transformers which were restricted by existing transformers
Injection_TX_restricted = arcpy.SelectData_management (Treatment_SA, "Facilities")
Injection_TX_restricted = arcpy.SelectLayerByAttribute_management (Injection_TX_restricted, "NEW_SELECTION",'"Status"= 3' )
arcpy.MakeFeatureLayer_management(Injection_TX_restricted,"Injection_TX_restricted")


#Export polygon layer
Treatment_Polygons = arcpy.SelectData_management (Treatment_SA, "Polygons")
Treatment_Polygons = Treatment_Polygons.getOutput(0)
Treatment_Polygons_withArea = arcpy.CalculateAreas_stats (Treatment_Polygons, "Treatment_Polygons")



#arcpy.MakeFeatureLayer_management(Treatment_Polygons_withArea,"Treatment_Polygons_Standard",'"F_AREA" >= 10000' )
arcpy.MakeFeatureLayer_management(Treatment_Polygons_withArea,"Treatment_Polygons_Small",'"F_AREA" <= 10000' )



##T3##
#It is possible that the resulting polygon from the previous step is <10,000 sq meters or 
#if an injection TX is completely engulfed in existing TX SA. 
#In this case, a new SA is drawn extending 150m from the injection TX in all possible directions. 
#This was the case with 3 treatment sites in Dansoman.



if arcpy.management.GetCount('Treatment_Polygons_Small')[0] > "0":     
	Injection_TX_Alt = arcpy.SelectLayerByLocation_management (Injection_TX, "INTERSECT", 'Treatment_Polygons_Small', "15 Meters")
	arcpy.MakeFeatureLayer_management(Injection_TX_Alt,"Injection_TX_Alt")
	#Injection_TX_Alt = Injection_TX_Alt.getOutput(0)
	Treatment_Alt_SA = arcpy.na.MakeServiceAreaLayer (network, district+"_Treatment_Alt_SA", "Length", "TRAVEL_FROM", "150" , "DETAILED_POLYS", "NO_MERGE" , "DISKS", "NO_LINES" , "NON_OVERLAP", "NO_SPLIT", Feeders , "", "", "", "TRIM_POLYS", distance_from_line)
	#Treatment_Alt_SA = Treatment_Alt_SA.getOutput(0)
	arcpy.na.AddLocations (Treatment_Alt_SA, "Facilities", Injection_TX_Alt, "", "25 Meters")
	arcpy.na.AddLocations (Treatment_Alt_SA, "Facilities", Injection_TX_restricted, "", "25 Meters")
	arcpy.na.Solve(Treatment_Alt_SA,"SKIP", "CONTINUE")
	#CHECK FOR ERRORS
	Treatment_Polygons_Alt = arcpy.SelectData_management (Treatment_SA, "Polygons")
	Treatment_Polygons_Alt = arcpy.MakeFeatureLayer_management(Treatment_Polygons_Alt, "Treatment_Polygons_Alt")
	#arcpy.SaveToLayerFile_management (Treatment_Polygons_Alt, "Treatment_Polygons_Alt")


else:
	Treatment_Polygons_Standard = arcpy.MakeFeatureLayer_management(Treatment_Polygons_withArea,"Treatment_Polygons_Standard",'"F_AREA" >= 10000' )


##T4##
#The result is area outlines either containing or directly adjacent to an Injection TX.
#Centroid coordinates are given to each site for feild staff to locate each site

#Collect all sites into 1 layer
arcpy.Merge_management ([Treatment_Polygons_Standard, Treatment_Polygons_Alt], "Treatment_Sites")

##Visually Inspect Results. Check To Make Sure all requirements are met. If not, then create polygons of outliers mannually

#Calculate site centroids
arcpy.AddGeometryAttributes_management('Treatment_Sites',"CENTROID")


#Adding Site IDs may be done mannually
#arcpy.AddField_management('Treatment_Sites',"Site_ID", "TEXT","" ,"",50,"","","","")
#arcpy.CalculateField_management('Treatment_Sites',"Site_ID", '!OBJECTID' + district_siteID_range, "PYTHON","")


arcpy.FeatureClassToShapefile('Treatment_Sites', "C:/PATH/folder")

###########END##########

