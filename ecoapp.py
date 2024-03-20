import streamlit as st
import pandas as pd

from insulation_calc.calculator import CommonCalculator
from insulation_calc.common.table_row import TableRow

st.write("""
# Калькулятор утепления Эковатой

*Не оферта
""")

st.sidebar.header('Задайте параметры расчета')


def user_input_features():
    sq = st.sidebar.number_input("Площадь перекрытия, м2", key='sqr_floor')
    # sq = st.sidebar.slider('Площадь перекрытия, м2', 10, 500, 100, key='sqr_floor')
    wi = st.sidebar.number_input('Толщина перекрытия, мм', key='width_floor')
    st.sidebar.radio('Нужна ли подготовка к утеплению?', ["Не нужна/Делаю своими силами", "Нужна"], horizontal=False,
                     key="is_floor_dop_work")
    sq_wall = st.sidebar.number_input('Площадь стен, м2', key='sqr_wall')
    wi_wall = st.sidebar.number_input('Толщина стен, мм', key='width_wall')
    st.sidebar.radio('Нужна ли подготовка к утеплению?', ["Не нужна/Делаю своими силами", "Нужна"],
                     key="is_wall_dop_work")
    sq_roof = st.sidebar.number_input('Площадь кровли, м2', key='sqr_roof')
    wi_roof = st.sidebar.number_input('Толщина кровли, мм', key='width_roof')
    st.sidebar.radio('Нужна ли подготовка к утеплению?', ["Не нужна/Делаю своими силами", "Нужна"],
                     key="is_roof_dop_work")
    aaa = st.sidebar.radio('Материал фасада дома', ["Кирпич/Газобетон", "Дерево"], index=1, key="is_wood_house")
    data = {'Площадь перекрытия, м2': sq,
            'Толщина перекрытия, мм': wi,
            'Площадь стен, мм': sq_wall,
            'Толщина стен, мм': wi_wall,
            'Площадь кровли, мм': sq_roof,
            'Толщина кровли, мм': wi_roof,
            }
    features = pd.DataFrame(data, index=[0])
    return features


df = user_input_features()

st.subheader('Расчет для параметров:')
st.table(df)

is_dop_work = lambda dop_work: True if dop_work == "Нужна" else False
wood_house = lambda is_wood_house: True if is_wood_house == "Дерево" else False

common_calc = CommonCalculator(
    sqr_floor=st.session_state.sqr_floor,
    width_floor=st.session_state.width_floor,
    sqr_wall=st.session_state.sqr_wall,
    width_wall=st.session_state.width_wall,
    sqr_roof=st.session_state.sqr_roof,
    width_roof=st.session_state.width_roof,
    is_wood_house=wood_house(st.session_state.is_wood_house),
    is_floor_dop_work=is_dop_work(st.session_state.is_floor_dop_work),
    is_wall_dop_work=is_dop_work(st.session_state.is_wall_dop_work),
    is_roof_dop_work=is_dop_work(st.session_state.is_roof_dop_work),
)
materials_data = common_calc.calculate_dop_work_materials()
data_table = [TableRow(**v).get_row() for _, v in materials_data.items()]

st.subheader('Материалы:')
st.dataframe(data_table, width=1000,)

works_data = common_calc.calculate_dop_work_costs()
data_table = [TableRow(**v).get_row() for _, v in works_data.items()]

st.subheader('Работы:')
st.dataframe(data_table, width=1000, use_container_width=True)
