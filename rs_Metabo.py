# Auteur : Julie BOGOIN
# 03/01/2022

import pandas

print('\n########################################')
print('Recherche de rs communs entre deux beds.')
print('########################################\n')


### Import des fichiers bruts

df_psl = pandas.read_csv("PSL_DIACHI-v7_1000012013_hg19_allelic_06Jul2021_capture_targets.bed", sep='\t')
header_psl = ['psl_chrom', 'psl_start', 'psl_stop', 'psl_name']
df_psl.columns = header_psl[:len(df_psl.columns)]

df_cch = pandas.read_csv("CCH_MonogNiptV3_hg19_21aug2019_capture_targets.bed", sep='\t')
header_cch = ['cch_chrom', 'cch_start', 'cch_stop', 'cch_name']
df_cch.columns = header_cch[:len(df_cch.columns)]

### Selectionner les positions entre 42000040 et 46500000

df_psl = df_psl[df_psl['psl_start'].between(42000040, 46500000)]
df_cch = df_cch[df_cch['cch_start'].between(42000040, 46500000)]

### Supprimer les lignes dont la colonne name est vide

df_psl.dropna(subset=['psl_name'], inplace=True)
df_cch.dropna(subset=['cch_name'], inplace=True)

### Supprimer les lignes dont la colonne name ne contient pas de rs

# Recuperer les index des lignes pour lesquels la colonne name ne contient pas rs
index_rs_psl = df_psl[ df_psl['psl_name'].str.contains('rs') == False ].index
# Supprimer les lignes du dataframe
df_psl.drop(index_rs_psl, inplace=True)

# Recuperer les index des lignes pour lesquels la colonne name ne contient pas rs
index_rs_cch = df_cch[ df_cch['cch_name'].str.contains('rs') == False ].index
# Supprimer les lignes du dataframe
df_cch.drop(index_rs_cch, inplace=True)

### Supprimer les lignes dont la colonne chrom n'est pas 7

# Recuperer les index des lignes pour lesquels le chrom n'est pas 7
index_7_psl = df_psl[ df_psl['psl_chrom'] != 'chr7' ].index
# Supprimer les lignes du dataframe
df_psl.drop(index_7_psl, inplace=True)

# Recuperer les index des lignes pour lesquels le chrom n'est pas 7
index_7_cch = df_cch[ df_cch['cch_chrom'] != 'chr7' ].index
# Supprimer les lignes du dataframe
df_cch.drop(index_7_cch, inplace=True)

### Transformer la colonne name en une liste de rs

df_psl['psl_name'] = df_psl.psl_name.str.split(";", expand=False)
df_cch['cch_name'] = df_cch.cch_name.str.split(";", expand=False)

### Creer le dataframe final PSL

df_list_psl = []

for i in df_psl.index:

    if len(df_psl['psl_name'][i]) == 1:
        if 'rs' in df_psl['psl_name'][i] :
            line_list = []
            line_list.append(df_psl['psl_chrom'][i])
            line_list.append(df_psl['psl_start'][i])
            line_list.append(df_psl['psl_stop'][i])
            line_list.append(rs)
            df_list_psl.append(line_list)

    if len(df_psl['psl_name'][i]) > 1:
        for rs in df_psl['psl_name'][i]:
            if 'rs' in rs :
                line_list = []
                line_list.append(df_psl['psl_chrom'][i])
                line_list.append(df_psl['psl_start'][i])
                line_list.append(df_psl['psl_stop'][i])
                line_list.append(rs)
                df_list_psl.append(line_list)

final_psl = pandas.DataFrame(df_list_psl, columns = header_psl)

### Creer le dataframe final CCH

df_list_cch = []

for i in df_cch.index:

    if len(df_cch['cch_name'][i]) == 1:
        if 'rs' in df_cch['cch_name'][i] :
            line_list = []
            line_list.append(df_cch['cch_chrom'][i])
            line_list.append(df_cch['cch_start'][i])
            line_list.append(df_cch['cch_stop'][i])
            line_list.append(rs)
            df_list_cch.append(line_list)

    if len(df_cch['cch_name'][i]) > 1:
        for rs in df_cch['cch_name'][i]:
            if 'rs' in rs :
                line_list = []
                line_list.append(df_cch['cch_chrom'][i])
                line_list.append(df_cch['cch_start'][i])
                line_list.append(df_cch['cch_stop'][i])
                line_list.append(rs)
                df_list_cch.append(line_list)

final_cch = pandas.DataFrame(df_list_cch, columns = header_cch)

### DATAFRAME FINAL

final = final_psl.merge(final_cch, left_on='psl_name', right_on='cch_name', how='inner')
del final['psl_chrom']
del final['cch_chrom']

### Export vers Excel

final.to_excel("output.xlsx", sheet_name='rs_communs_PSL_CCH')
print('Fichier Output genere.')  

print('\n#######################################')
print('############# JOB DONE ! ############## ')
print('#######################################\n')