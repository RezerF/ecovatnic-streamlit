import streamlit as st
import pandas as pd

from insulation_calc.calculator import CommonCalculator
from insulation_calc.common.table_row import TableRow

st.write("""
# Калькулятор утепления Эковатой

*Не оферта
""")

def user_input_features():
    st.sidebar.header("=============Перекрытие=============")
    sq = st.sidebar.number_input("Площадь перекрытия, м2", key='sqr_floor')
    wi = st.sidebar.number_input('Толщина перекрытия, мм', key='width_floor')
    st.sidebar.radio('Нужна ли подготовка к утеплению?', ["Не нужна/Делаю своими силами", "Нужна"],
                     key="is_floor_dop_work")
    st.sidebar.radio('Через прокол?', ["Да", "Нет, насыпь"],
                     key="is_spine", index=1)

    st.sidebar.header("================Стены================")
    sq_wall = st.sidebar.number_input('Площадь стен, м2', key='sqr_wall')
    wi_wall = st.sidebar.number_input('Толщина стен, мм', key='width_wall')
    st.sidebar.number_input('Площадь высотой более 3 метров, м2', key='high_three_wall')
    st.sidebar.number_input('Площадь высотой более 6 метров, м2', key='high_six_wall')
    st.sidebar.number_input('Количество окон/дверей, шт', key='count_window')
    st.sidebar.number_input('Количество вент-каналов, шт', key='count_went_kanal')
    st.sidebar.radio('Нужна ли подготовка к утеплению?', ["Не нужна/Делаю своими силами", "Нужна"],
                     key="is_wall_dop_work")

    st.sidebar.header("===============Кровля===============")
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
to_bool_spine = lambda is_spine: True if is_spine == "Да" else False

common_calc = CommonCalculator(
    sqr_floor=st.session_state.sqr_floor,
    width_floor=st.session_state.width_floor,
    is_spine=to_bool_spine(st.session_state.is_spine),
    sqr_wall=st.session_state.sqr_wall,
    width_wall=st.session_state.width_wall,
    high_three_wall=st.session_state.high_three_wall,
    high_six_wall=st.session_state.high_six_wall,
    count_window=st.session_state.count_window,
    count_went_kanal=st.session_state.count_went_kanal,
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

amount_prices = [v["amount_price"] for _, v in materials_data.items()]
total = sum(amount_prices)
st.markdown(f"#### Итого материалы:  ___ {total}___ руб.   ")
st.markdown("    ")
st.markdown("    ")
st.markdown("    ")

works_data = common_calc.calculate_dop_work_costs()
data_table = [TableRow(**v).get_row() for _, v in works_data.items()]

st.subheader('Работы:')
st.dataframe(data_table, width=1000, use_container_width=True)

amount_prices = [v["amount_price"] for _, v in works_data.items()]
total = sum(amount_prices)
st.markdown(f"#### Итого работы:  ___ {total}___ руб.")
