#Read in growth data 

base_dir = "G:/.shortcut-targets-by-id/0B3ejcGO9fA5eYXlHMW9tekVERmc/JB labs documents/Updated_JB_documents_2019/JB LAB_Projects/biofilm_qtl"

biolector_data = read.csv(paste(base_dir, "/data/biolector/20241018_JB50_JB759_JB914_JB953_EMM_YES_EMM-P.csv", sep = ""), skip=23)

biolector_data_biomass = biolector_data[(biolector_data$READING... == "1") | (biolector_data$READING... == "TIME [h] ->"),]
biolector_data_biomass = biolector_data_biomass[-c(2,3,4)]
biolector_data_biomass[1,1]='time'





