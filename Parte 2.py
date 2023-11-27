#!/usr/bin/env python
# coding: utf-8

# # Parte 2 - Caso Práctico 1

# #### Importacion  Librerias

# In[1]:


import pandas as pd
import numpy as np
import warnings 
from datetime import date

today = np.datetime64(date.today())


# In[2]:


warnings.filterwarnings('ignore')


# In[3]:


data = pd.read_excel("../Datos_empleados_Prueba_técnica.xlsx")


# ####  Analisis de informacion, limpieza y transformacion

# In[4]:


data.head(2)


# In[5]:


print("Numero de registros: ",len(data))


# In[6]:


data.columns


# In[7]:


data.columns[data.isnull().sum() > 0]


# ####  Las columnas relevantes que se deben rellenar son: Fecha de nacimiento,Fecha de ingreso,Categoría terminación,Razón terminación

# #### Se completan las fechas de ingreso en este caso con la misma fecha de contratacion

# In[8]:


data["Fecha de ingreso"][data["Fecha de ingreso"].isnull()] = data["Fecha de contratación"][data["Fecha de ingreso"].isnull()]


# #### De las personas con fecha de terminacion, 3  no tienen categoria de terminacion y razon de terminacion; se evidencia que 2 de estas personas su fecha de terminacion es unos dias luego de haber ingresado por lo que su causa probable fue de renuncia, se supone esto mismo para la otra persona por el rol que tenia ; como la renuncia es una causa no planeada se llevan a esta categoria. 

# ## Para los analisis se parte la información en personas activas y retiradas, ya que en teoría vienen de eventos diferentes (maestra actual y maestra histórica respectivamente)

# In[9]:


data_activos = data[data["Fecha de terminación"].isnull()].reset_index(drop=True)


# In[10]:


data_retiros = data[data["Fecha de terminación"].notnull()].reset_index(drop=True)


# In[11]:


print("Personas activas: ", len(data_activos))


# In[12]:


print("Personas Retiradas: ", len(data_retiros))


# In[15]:


data_retiros["Categoría terminación"].fillna('Unplanned',inplace=True)


# In[16]:


data_retiros["Razón terminación"].fillna('Resignation',inplace=True)


# #### Se encuentra que el 31.6% de los empleados activos no cuentan con la edad

# In[17]:


str(round((3837/12132),3)*100)+'%'


# #### Se encuentra que el 33.7% de los empleados retirados no cuentan con la edad

# In[18]:


str(round((1055/3135),3)*100)+'%'


# #### Para el tratamiento se rellenan temporalmente las fechas de nacimiento vacias con una fecha cualquiera y se calcula la edad

# In[74]:


data_activos['Fecha de nacimiento'].fillna(np.datetime64('1900-01-01'),inplace=True)


# In[75]:


data_activos["Edad"] = (today - data_activos['Fecha de nacimiento']).dt.days/365


# In[76]:


data_activos["Edad"] = data_activos["Edad"].astype('int')


# #### Estadisticos de la edad: se concluye que se puede usar la media , mediana o moda indistintamente debido a que son confiables ya que la desviacion estandar es pequeña comparada con estas medidas

# In[98]:


data_activos["Edad"][data_activos["Edad"] != 123].describe()


# In[110]:


mean = data_activos["Edad"][data_activos["Edad"] != 123].mean()
std = data_activos["Edad"][data_activos["Edad"] != 123].std()
mode = data_activos["Edad"][data_activos["Edad"] != 123].mode()


# In[142]:


print("Coeficiente de variacion Edad: ",(std/mean)*100)


# #### Al ser el coeficiente de variacion menor que el 30% se considera que los datos son homogeneos, así finalmente se comprueba la hipótesis que se tenia

# In[124]:


val_123 = data_activos["Edad"][data_activos["Edad"] == 123].index


# In[126]:


data_activos["Edad"].iloc[val_123]  = 42


# In[137]:


data_activos.to_excel("data_activos.xlsx",index=False)


# In[138]:


data_retiros.to_excel("data_retiros.xlsx",index=False)


# ## *******Consideracion inicial sobre tasa de rotacion es que no va a ser la real ya que se está comparando maestra actual vs retiros, la comparacion real es maestra historica vs retiros*******

# In[140]:


data_retiros["Satisfacción Laboral"].describe()


# In[144]:


data_retiros["Desempeño"].describe()


# # *Insights

# ####  Se crea una medida del promedio del desempeño para las personas que se han retirado y se encuentra que en general las personas que se han ido han tenido buen desempeño; fuga de talentos (?)

# #### El año donde se presentó mayor tasa de rotacion es 2019 , algun evento especial (?)

# #### El área que presentó mayor rotación de todas es produccion, comportamiento normal del area (?) 

# #### Se crea medida del promedio de la satisfacción de los empleados al retirarse es muy baja < 5, como se está acompañando el proceso de retiro (?), algo particular es que las 2 áreas con menor cantidad de retiros que son HR (4) y management con (3) tienen la satisfaccion excesivamente baja < 3, analizar casos individualmente (?), percepción generalizada sobre dichas áreas (?)

# # *Modelo predictivo de factores que contribuyen a la rotación

# ####  A priori de las variables disponibles en los datos usaría: genero,tipo de jornada, Area, Razon terminacion, satisfaccion laboral, desempeño y si han sido promovidos; se plantearía un arbol de decisión en donde el modelo alimentado decida sobre las caracteristicas mas relevantes, y posiblemnte se pueda combinar con algun tipo de regresion , para calcular una variable target de probabilidad de fuga de una persona

# # *Sugerencias Sobre Insights

# #### Para reducir la rotación se recomienda , analizar la satisfacción en general de los empleados ya que se considera muy baja y ver las motivaciones que los ha llevado a sentirse así además de que se considera que han tenido buen desempeño en promedio de 84% y que quizá no se esté presentando una fuga de talentos (con algun proceso de entrevistas de retiro), analizar en detalle el area de produccion y como tratar de reducir al maximo su rotacion, sea normal o no el comportamiento para esta área (algun plan de incentivos especial para estos roles, ya que el si han sido promovidos o no no fue relevante y por eso no se agregó a dicho análisis) , incluyendo sus cargos ya que puede no tengan proyeccion de carrera (se ven 3 cargos)

# In[ ]:




