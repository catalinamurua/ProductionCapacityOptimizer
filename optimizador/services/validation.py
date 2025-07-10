class ValidacionParametros:
    # Constante que define el máximo de horas disponibles por día para una máquina
    MAX_HOURS_PER_DAY = 24

    def __init__(self, data_row):
        """
        Constructor que recibe una fila de datos (pd.Series) con los parámetros ya validados por formato.
        
        Args:
            data_row (pd.Series): Una fila del DataFrame con los parámetros a validar.
        """
        self.data = data_row
        
        # Lista de campos que se validarán en los métodos de esta clase
        self.campos = [
            'Product_A_Production_Time_Machine_1', 'Product_A_Production_Time_Machine_2',
            'Product_B_Production_Time_Machine_1', 'Product_B_Production_Time_Machine_2',
            'Machine_1_Available_Hours', 'Machine_2_Available_Hours',
            'Price_Product_A', 'Price_Product_B'
        ]

    def ejecutar_validaciones(self):
        """
        Ejecuta todas las validaciones en orden.
        Lanza un ValueError si alguna validación falla.
        """
        self._validar_no_nulos()
        self._validar_no_negativos()
        self._validar_maximo_diario()
        self._validar_maquinas_mayores_cero()
        self._validar_hay_capacidad()
        self._validar_hay_demanda()
        self._validar_se_puede_producir_algo()
        self._validar_tiempos_por_producto_y_maquina()

    def _validar_no_nulos(self):
        """
        Verifica que ninguno de los campos especificados sea nulo.
        """
        if not self.data[self.campos].notnull().all():
            raise ValueError("Existen parámetros nulos o faltantes en los datos.")

    def _validar_no_negativos(self):
        """
        Verifica que ningún parámetro sea negativo.
        """
        for campo in self.campos:
            if self.data[campo] < 0:
                raise ValueError(f"El parámetro '{campo}' no puede ser negativo.")

    def _validar_maximo_diario(self):
        """
        Verifica que las horas disponibles de las máquinas no excedan las 24 horas diarias.
        """
        if self.data['Machine_1_Available_Hours'] > self.MAX_HOURS_PER_DAY:
            raise ValueError("La Máquina 1 no puede tener más de 24 horas disponibles por día.")
        if self.data['Machine_2_Available_Hours'] > self.MAX_HOURS_PER_DAY:
            raise ValueError("La Máquina 2 no puede tener más de 24 horas disponibles por día.")

    def _validar_maquinas_mayores_cero(self):
        """
        Verifica que las horas disponibles de cada máquina sean mayores que cero.
        """
        if self.data['Machine_1_Available_Hours'] <= 0:
            raise ValueError("La Máquina 1 debe tener más de 0 horas disponibles.")
        if self.data['Machine_2_Available_Hours'] <= 0:
            raise ValueError("La Máquina 2 debe tener más de 0 horas disponibles.")

    def _validar_hay_capacidad(self):
        """
        Verifica que no ambas máquinas tengan cero horas disponibles simultáneamente.
        Esta validación es redundante si _validar_maquinas_mayores_cero se usa,
        pero se mantiene para seguridad.
        """
        if self.data['Machine_1_Available_Hours'] == 0 and self.data['Machine_2_Available_Hours'] == 0:
            raise ValueError("Ambas máquinas tienen 0 horas disponibles. No se puede producir nada.")

    def _validar_hay_demanda(self):
        """
        Verifica que al menos uno de los productos tenga precio positivo,
        asegurando que hay ingresos posibles.
        """
        if self.data['Price_Product_A'] <= 0 and self.data['Price_Product_B'] <= 0:
            raise ValueError("Ambos productos tienen precios cero o negativos. No hay ingresos posibles.")

    def _validar_se_puede_producir_algo(self):
        """
        Verifica que sea posible producir al menos una unidad de alguno de los productos
        con la capacidad disponible en alguna de las máquinas.
        """
        puede_A = (
            self.data['Product_A_Production_Time_Machine_1'] <= self.data['Machine_1_Available_Hours'] or
            self.data['Product_A_Production_Time_Machine_2'] <= self.data['Machine_2_Available_Hours']
        )
        puede_B = (
            self.data['Product_B_Production_Time_Machine_1'] <= self.data['Machine_1_Available_Hours'] or
            self.data['Product_B_Production_Time_Machine_2'] <= self.data['Machine_2_Available_Hours']
        )

        if not (puede_A or puede_B):
            raise ValueError("No se puede producir ni una unidad de ningún producto con la capacidad disponible.")

    def _validar_tiempos_por_producto_y_maquina(self):
        """
        Verifica que el tiempo requerido para producir UNA unidad de cada producto
        en cada máquina no exceda la disponibilidad de la máquina.
        """
        t_a1 = self.data['Product_A_Production_Time_Machine_1']
        t_a2 = self.data['Product_A_Production_Time_Machine_2']
        t_b1 = self.data['Product_B_Production_Time_Machine_1']
        t_b2 = self.data['Product_B_Production_Time_Machine_2']

        t_m1 = self.data['Machine_1_Available_Hours']
        t_m2 = self.data['Machine_2_Available_Hours']

        errores = []
        if t_a1 > t_m1:
            errores.append("Tiempo requerido para Producto A en Máquina 1 excede disponibilidad.")
        if t_a2 > t_m2:
            errores.append("Tiempo requerido para Producto A en Máquina 2 excede disponibilidad.")
        if t_b1 > t_m1:
            errores.append("Tiempo requerido para Producto B en Máquina 1 excede disponibilidad.")
        if t_b2 > t_m2:
            errores.append("Tiempo requerido para Producto B en Máquina 2 excede disponibilidad.")

        if errores:
            raise ValueError(" | ".join(errores))
