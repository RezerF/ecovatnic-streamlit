import streamlit as st
import pandas as pd

from insulation_calc.calculator import CommonCalculator, EcovataCalculator
from insulation_calc.common.constants import Plotnost
from insulation_calc.common.table_row import TableRow

import hmac
import streamlit as st


# auth streamlit
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.


# wide mode default
def wide_space_default():
    st.set_page_config(layout="wide")


wide_space_default()
st.write("""
# Калькулятор утепления Эковатой

*Не оферта
""")


def user_input_features():
    st.logo("images/android-chrome-192x192.png", link="https://eco-vatnik.ru", )
    st.sidebar.header("=========Необходимо учесть==========")
    st.sidebar.toggle("Строительство лесов", key="build_lesa")
    st.sidebar.number_input("Демонтаж без утилизации, м2", key='demontaj')
    st.sidebar.number_input("Пробивание технологических отверстий в ленте, шт", key="destroy_beton")

    st.sidebar.header("=======Коэффициент сложности======")
    st.sidebar.slider("Коэф", min_value=1.0, max_value=4.0, step=0.25, key='ratio')
    st.sidebar.header("=============Перекрытие=============")
    sq = st.sidebar.number_input("Площадь перекрытия, м2", key='sqr_floor')
    wi = st.sidebar.number_input('Толщина перекрытия, мм', key='width_floor')
    st.sidebar.radio('Нужна ли подготовка к утеплению?', ["Не нужна/Делаю своими силами", "Нужна"],
                     key="is_floor_dop_work")
    st.sidebar.radio('Через прокол?', ["Да", "Нет, насыпь"],
                     key="is_spine")

    st.sidebar.header("================Стены================")
    sq_wall = st.sidebar.number_input('Площадь стен, м2', key='sqr_wall')
    wi_wall = st.sidebar.number_input('Толщина стен, мм', key='width_wall')
    st.sidebar.radio('Нужна ли подготовка к утеплению?', ["Не нужна/Делаю своими силами", "Нужна"],
                     key="is_wall_dop_work")

    st.sidebar.header("===============Кровля===============")
    sq_roof = st.sidebar.number_input('Площадь кровли, м2', key='sqr_roof')
    wi_roof = st.sidebar.number_input('Толщина кровли, мм', key='width_roof')
    st.sidebar.radio('Нужна ли подготовка к утеплению?', ["Не нужна/Делаю своими силами", "Нужна"],
                     key="is_roof_dop_work")
    st.sidebar.radio('Материал фасада дома', ["Кирпич/Газобетон", "Дерево"], index=1, key="is_wood_house")
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
    sqr_wall=st.session_state.sqr_wall,
    width_wall=st.session_state.width_wall,
    sqr_roof=st.session_state.sqr_roof,
    width_roof=st.session_state.width_roof,
    is_wood_house=wood_house(st.session_state.is_wood_house),
    is_floor_dop_work=is_dop_work(st.session_state.is_floor_dop_work),
    is_wall_dop_work=is_dop_work(st.session_state.is_wall_dop_work),
    is_roof_dop_work=is_dop_work(st.session_state.is_roof_dop_work),
    is_spine=to_bool_spine(st.session_state.is_spine),
    ratio=st.session_state.ratio,
    demontaj=st.session_state.demontaj,
    build_lesa=st.session_state.build_lesa,
    destroy_beton=st.session_state.destroy_beton,
)
materials_data = common_calc.calculate_dop_work_materials()
data_table = [TableRow(**v).get_row() for _, v in materials_data.items()]

st.subheader('Материалы:')
st.dataframe(data_table, use_container_width=True)

amount_prices = [v["amount_price"] for _, v in materials_data.items()]
total_materials = sum(amount_prices)
st.markdown(f"#### Итого материалы:  ___ {total_materials}___ руб.   ")
st.markdown("    ")

st.subheader('Работы:')

works_data = common_calc.calculate_dop_work_costs()
data_table = [TableRow(**v).get_row() for _, v in works_data.items()]

st.dataframe(data_table, width=1000, use_container_width=True)

amount_prices = [v["amount_price"] for _, v in works_data.items()]
total_works = sum(amount_prices)
st.markdown(f"#### Итого работы:  ___ {total_works}___ руб.")
st.subheader('', divider='rainbow')
st.markdown(f"#### Итого работы + материалы:  ___ {total_materials + total_works}___ руб.")

### Объемы
ecovata_calc_floor = EcovataCalculator(
    sqr=st.session_state.sqr_floor,
    width=st.session_state.width_floor,
    plotnost=Plotnost.INCLINED if to_bool_spine(st.session_state.is_spine) else Plotnost.HORISONTAL)

ecovata_calc_wall = EcovataCalculator(
    sqr=st.session_state.sqr_wall,
    width=st.session_state.width_wall,
    plotnost=Plotnost.VERTICAL)

ecovata_calc_roof = EcovataCalculator(
    sqr=st.session_state.sqr_roof,
    width=st.session_state.width_roof,
    plotnost=Plotnost.VERTICAL)

st.subheader('', divider='rainbow')
st.subheader('')
st.subheader('Объемы:')
if to_bool_spine(st.session_state.is_spine):
    vol_plontost_55 = ecovata_calc_floor.volume_calculate + ecovata_calc_roof.volume_calculate
    vol_plontost_35 = 0
else:
    vol_plontost_55 = ecovata_calc_roof.volume_calculate
    vol_plontost_35 = ecovata_calc_floor.volume_calculate
st.markdown(f'35кг/м3: ___ {vol_plontost_35}___куб.м.')
st.markdown(f'55кг/м3: ___ {vol_plontost_55}___куб.м.')
st.markdown(f'65кг/м3: ___ {ecovata_calc_wall.volume_calculate}___куб.м.')
