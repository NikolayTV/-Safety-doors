# Solaris Safety-doors
Web morda - https://github.com/opmoje/003-frontend

Демо - http://94.41.16.201:8081/i

##Описание подхода

### Инструменты 

- PythonPCL (https://github.com/strawlab/python-pcl)
- Open3d (https://github.com/intel-isl/Open3D)

### Проделанная работа по CV

- Загрузка `.pcd` данных и понижение размерности облака точек
- Первичная кластеризация облака точек при помощи `kd_tree`(https://github.com/strawlab/python-pcl/blob/master/examples/kdtree.py) и `EuclideanClusterExtraction`(https://github.com/strawlab/python-pcl/blob/master/examples/official/Segmentation/cluster_extraction.py)
- Извлечение дескрипторов из полученных кластеров при помощи VFH (Viewpoint Features Histogram) - https://pcl.readthedocs.io/projects/tutorials/en/latest/vfh_estimation.html#estimating-vfh-features * Так как поддержка Python-pcl была прекращена, в библиотеке не был реализован метод для получения VFH, что было замечено очень поздно. 
  Нами была создана кастомная реализация метода VFH на основании описания и `C++` реализации для оригинальной версии PCL
- Помимо дескриптора VFH мы используем и другие статистики - средние значения кластера по осям, матрицы ковариации, размер кластера.
- Классификация извлеченных дескрипторов на выборке из 26 объектов из обучающей выборки. SVC с линейным ядром показал наиболее высокий и робастный результат на Stratified KFold.
- Запись результата в `JSON`
  
### Web morda демонстрации решения и бэк
- Бэк делает запрос в MLCore, для которого написан REST API
- На выход получает json с откластиризованными и классифицированными предсказаниями
  