# -Safety-doors
Web-morda - https://github.com/opmoje/003-frontend

IN PROGRESS

We try to prepare Docker, for you - code reviewers

##Описание подхода

### Инструменты 

- PythonPCL (https://github.com/strawlab/python-pcl)
- Open3d (https://github.com/intel-isl/Open3D)

### Этапы работы системы
- Загрузка `.pcd` данных и понижение размерности облака точек
- Первичная кластеризация облака точек при помощи `kd_tree`(https://github.com/strawlab/python-pcl/blob/master/examples/kdtree.py) и `EuclideanClusterExtraction`(https://github.com/strawlab/python-pcl/blob/master/examples/official/Segmentation/cluster_extraction.py)
- Извлечение дескрипторов из полученных кластеров при помощи VFH (Viewpoint Features Histogram) - https://pcl.readthedocs.io/projects/tutorials/en/latest/vfh_estimation.html#estimating-vfh-features * Так как поддержка Python-pcl была прекращена, в библиотеке не был реализован метод для получения VFH, нами была создана кастомная реализация метода VFH на основании описания и `C++` реализации для оригинальной версии PCL
- Классификация извлеченных дескрипторов линейной моделью
- Запись результата в `JSON`
- По запросу из фронтенда в MLCore результат обработки отправляется для отображения в веб морду 
