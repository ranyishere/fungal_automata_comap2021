import pandas as pd


"""
valid_colors = [
    (255,215,0, 1),
    (255,177,78, 1),
    (250,135,117, 1),
    (234,95,148, 1),
    (205,52,181, 1),
    (157,2,215, 1),
    (0,0,255, 1)
]
"""

valid_colors = [
    (255/255,215/255,0, 1),
    (255/255,177/255,78/255, 1),
    (250/255,135/255,117/255, 1),
    (234/255,95/255,148/255, 1),
    (205/255,52/255,181/255, 1),
    (157/255,2/255,215/255, 1),
    (0,0, 255/255, 1)
]

enemy_color = [
            (255/255, 0, 0, 1)
        ]



fungal_names = [
            'p.gilv.n',
            'x.sub.s',
            'p.pend.n',
            'm.trem.n',
            't.chion.n',
            'p.rufa.acer.s'
        ]

fungal_names_2 = [
            'p.gilv', 'x.sub', 'p.pend',
            'm.trem', 't.chion', 'p.rufa.acer'
            ]


def load_fungal_moist_data(name, model):
    """
    Load Fungal Moisture Data
    """
    data = pd.read_csv('fungal_biogeography/fungi_data/Fungi_moisture_curves.csv')
    moisture_data = data[data['species'] == name]
    moisture_data = moisture_data[moisture_data['type'] == 'smoothed']

    x = moisture_data['matric_pot']
    y = moisture_data['hyphal_rate']

    # model['matric_pot'] = x.values
    # model['hyphal_rate'] = y.values

    model['moisture'] = moisture_data


def load_fungal_temp_data(name, model):
    """
    Load Fungal Temperature Data
    """

    data = pd.read_csv('fungal_biogeography/fungi_data/Fungi_temperature_curves.csv')
    temp_data = data[data['species'] == name]
    temp_data = temp_data[temp_data['type'] == 'smoothed']
    x = temp_data['temp_c']
    y = temp_data['hyphal_rate']

    model['temperature'] = temp_data
    # model['temp_c'] = x.values
    # model['hyphal_rate'] = y.values
    # print("temp_data: ", temp_data['temp_c']==)


def load_fungal_traits(name, model):
    """
    Load Fungal Traits
    """

    # Density
    growth_rate_key = 'growth_rate'
    density_key = 'hyphal_density'
    comp_rank_key = 'competitive_rank'
    decomp_rank_key = 'decomp_rate'
    temp_niche_key = 'temp.niche.width'
    water_niche_key = 'water.niche.width'

    data = pd.read_csv('fungal_biogeography/fungi_data/atr_fungi3.csv')
    data_2 = pd.read_csv('fungal_biogeography/fungi_data/Fungal_trait_data.csv')

    species_data = data[data['species.id'] == name]
    species_data_2 = data_2[data_2['name3'] == name]

    # print("species_data.columns.values: ", species_data.columns.values)

    # print("spcies_data density: ", species_data[density_key])
    # exit()

    total_traits = {
                growth_rate_key: species_data[growth_rate_key].values[0],
                'density': species_data[density_key].values[0],
                'comp_rank': species_data[comp_rank_key].values[0],
                decomp_rank_key: species_data[decomp_rank_key].values[0],
                temp_niche_key: species_data_2[temp_niche_key],
                water_niche_key: species_data_2[water_niche_key]
            }

    model['traits'] = total_traits


total_fungi = {}
for ix, each_name in enumerate(fungal_names):
    current_fungi = {'name': each_name}
    name_1 = fungal_names[ix]
    name_2 = fungal_names_2[ix]

    load_fungal_moist_data(name_1, current_fungi)
    load_fungal_temp_data(name_1, current_fungi)
    load_fungal_traits(name_2, current_fungi)
    total_fungi[name_1] = current_fungi

    # total_fungi.append(current_fungi)

# print("total_fungi: ", total_fungi)
# exit()

class Cell(object):

    """
    Abstract Cell
    """

    def __init__(self):
        """
        Init
        """

        pass


class WoodCell(Cell):
    """
    Wood Cell My dude
    """

    def __init__(self, row, col, strength, moisture=0, temperature=0):
        """
        Init
        """

        # Remaining Mass
        self.strength = strength

        self.ref_color = valid_colors[0]
        # self.col_mod = 255 - self.strength*255.0
        # self.color = (self.ref_color[0], self.ref_color[1], self.ref_color[2], self.strength)
        self.color = (
                    self.ref_color[0],
                    self.ref_color[1],
                    self.ref_color[2],
                    self.strength*1.0
                )
        self.row = row
        self.col = col

        # Wood Properties
        self.density = 0
        self.moisture = 0

        self.moisture = moisture
        self.temperature = temperature


    def update_strength(self, amt):
        """
        Update
        """

        self.strength = amt
        self.color = (self.ref_color[0], self.ref_color[1], self.ref_color[2], self.strength)

    def __str__(self):
        return "<w str: {0} row: {1} col: {2} color: {3}>".format(self.strength, self.row, self.col, self.color)

    def __repr__(self):
        return "<w str: {0} row: {1} col: {2} color: {3}>".format(self.strength, self.row, self.col, self.color)


class FoodCell(WoodCell):

    def __init__(self, row, col, strength, wood_ext_rate=20.41, temperature=23.0):
        super().__init__(row, col, strength)
        self.ref_color = valid_colors[-3]
        # self.color = (self.ref_color[0], self.ref_color[1], self.ref_color[2], strength*1.0)
        self.color = (
                    self.ref_color[0],
                    self.ref_color[1],
                    self.ref_color[2],
                    self.strength*1.0
                )

        self.wood_ext_rate = wood_ext_rate
        self.temperature = temperature

class Qalba(WoodCell):

    def __init__(self, row, col, strength, moisture=-0.01, temperature=25):
        super().__init__(row, col, strength)
        self.ref_color = valid_colors[1]
        # self.color = (self.ref_color[0], self.ref_color[1], self.ref_color[2], strength*1.0)
        self.color = (
                    self.ref_color[0],
                    self.ref_color[1],
                    self.ref_color[2],
                    self.strength*1.0
                )

        self.wood_ext_rate = 11.41

        self.moisture = moisture
        self.temperature = temperature

    def __str__(self):
        return "<w qalba str: {0} row: {1} col: {2} color: {3}>".format(self.strength, self.row, self.col, self.color)

    def __repr__(self):
        return "<w qalba str: {0} row: {1} col: {2} color: {3}>".format(self.strength, self.row, self.col, self.color)




class Qvelutina(WoodCell):

    def __init__(self, row, col, strength, moisture=-0.01, temperature=25):
        super().__init__(row, col, strength, moisture, temperature)
        self.ref_color = valid_colors[0]
        # self.color = (self.ref_color[0], self.ref_color[1], self.ref_color[2], strength*1.0)
        self.color = (
                    self.ref_color[0],
                    self.ref_color[1],
                    self.ref_color[2],
                    self.strength*1.0
                )

        self.wood_ext_rate = 4.08

        self.moisture = moisture
        self.temperature = temperature


class Aglabra(WoodCell):

    def __init__(self, row, col, strength, moisture=-0.01, temperature=25):
        super().__init__(row, col, strength)
        self.ref_color = valid_colors[2]
        # self.color = (self.ref_color[0], self.ref_color[1], self.ref_color[2], strength*1.0)
        self.color = (
                    self.ref_color[0],
                    self.ref_color[1],
                    self.ref_color[2],
                    self.strength*1.0
                )

        self.wood_ext_rate = 12.2

        self.moisture = moisture
        self.temperature = temperature




class FungiCell(Cell):


    def __init__(self, row, col, strength=25, wood_strength=-0.01):
        """
        Init
        """

        self.time_born = 0

        self.weights = {
                '': 123
                }

        self.strength = strength
        self.wood_type = 'agar'

        self.ref_color = valid_colors[-1]
        self.color = (
                    self.ref_color[0],
                    self.ref_color[1],
                    self.ref_color[2],
                    self.strength*1.0
                )

        self.row = row
        self.col = col

        # Fungi Properties
        self.base_growth_rate = 0
        self.mono_culture_rate = 0
        self.growth_rate = 0.1
        self.hyphal_growth_rate = 0
        self.avg_density = 0.1

        self.temperature_growth = 0
        self.moisture_growth = 0

        self.defensive_ability = 0
        self.offensive_ability = 0 # Density/enemy_rowth_rate
        self.moisture_level = 0

        self.current_temperature = 0

        # wood properties
        self.base_wood_decomp = 0
        self.wood_decomposition_rate = self.base_wood_decomp + self.growth_rate**0.19 + self.avg_density**-0.21
        self.wood_strength = wood_strength

        self.moisture = 0
        self.temperature = 0


    def get_temp_growth(self, temp):

        # print("temp: ", temp)
        temp = round(temp, 2)
        try:
            temp_g = self.data['temperature'][self.data['temperature']['temp_c']==temp]['hyphal_rate'].values[0]

            return temp_g
        except IndexError:
            print("temp: ", temp)


    def get_total_growth(self):
        """
        Get total growth
        """

        w_1 = 0.05
        w_2 = 0.38
        w_3 = 0.32
        w_4 = 0.25


        tg = w_1*self.base_growth_rate + w_2*self.temperature_growth + w_3*self.moisture_growth + w_4*self.wood_growth
        return tg

    def calculate_total_growth(self, temp_g):
        w_1 = 0.05
        w_2 = 0.38
        w_3 = 0.32
        w_4 = 0.25

        tg = w_1*self.base_growth_rate + w_2*temp_g + w_3*self.moisture_growth + w_4*self.wood_growth
        return tg
    


    def update_strength(self, amt):
        """
        Update Strength
        """

        self.strength = amt
        
    def __str__(self):
        return "<f str: {0} row: {1} col: {2} color: {3}>".format(self.strength, self.row, self.col, self.color)

    def __repr__(self):
        return "<f str: {0} row: {1} col: {2} color: {3}>".format(self.strength, self.row, self.col, self.color)


class Pgilv(FungiCell):

    name = 'p.gilv.n'

    def __init__(self, row, col, strength, temperature=25, moisture=-0.01, wood_strength=1, wood_growth=11.41):
        super().__init__(row, col, strength, wood_strength)

        self.time_born = 0

        self.name = 'p.gilv.n'

        self.data = total_fungi[self.name]

        self.ref_color = valid_colors[-1]
        self.color = (
                    self.ref_color[0],
                    self.ref_color[1],
                    self.ref_color[2],
                    self.strength*1.0
                )

        self.moisture = round(moisture, 2)
        self.temperature = temperature

        self.base_decomp_rate = self.data['traits']['decomp_rate']
        self.base_growth_rate = self.data['traits']['growth_rate']

        self.avg_density = self.data['traits']['density']


        # Load competitiveness

        self.temperature_growth = self.get_temp_growth(temperature)
        self.moisture_growth = self.data['moisture'][self.data['moisture']['matric_pot']==self.moisture].values[0][2]

        # print(self.data['moisture']['matric_pot'].values)
        # print("self.moisture: ", self.moisture)

        # print("self.moisture: ", self.moisture)
        self.wood_growth = wood_growth

        # Calculate 
        self.mono_culture_rate = 0
        self.hyphal_growth_rate = 0

        self.comp_rank = self.data['traits']['comp_rank']

    
    def get_total_growth(self):
        """
        Get total growth
        """

        w_1 = 0.05
        w_2 = 0.38
        w_3 = 0.32
        w_4 = 0.25


        tg = w_1*self.base_growth_rate + w_2*self.temperature_growth + w_3*self.moisture_growth + w_4*self.wood_growth
        return tg

    def calculate_total_growth(self, temp_g):
        w_1 = 0.05
        w_2 = 0.38
        w_3 = 0.32
        w_4 = 0.25

        tg = w_1*self.base_growth_rate + w_2*temp_g + w_3*self.moisture_growth + w_4*self.wood_growth

        return tg
    


class Xsub(FungiCell):

    name = 'x.sub.s'

    def __init__(self, row, col, strength, temperature=25, moisture=-0.1, wood_strength=1, wood_growth=11.41):
        super().__init__(row, col, strength, wood_strength)

        self.name = 'x.sub.s'

        self.data = total_fungi[self.name]

        self.ref_color = valid_colors[-2]
        self.color = (
                    self.ref_color[0],
                    self.ref_color[1],
                    self.ref_color[2],
                    self.strength*1.0
                )


        # self.moisture = moisture

        self.moisture = round(moisture, 2)
        self.temperature = temperature

        self.base_decomp_rate = self.data['traits']['decomp_rate']
        self.base_growth_rate = self.data['traits']['growth_rate']

        self.avg_density = self.data['traits']['density']
        # Load competitiveness

        self.temperature_growth = self.get_temp_growth(temperature)
        self.moisture_growth = self.data['moisture'][self.data['moisture']['matric_pot']==self.moisture].values[0][2]

        self.wood_growth = wood_growth

        # Calculate 
        self.mono_culture_rate = 0
        self.hyphal_growth_rate = 0

        self.comp_rank = self.data['traits']['comp_rank']



class Ppend(FungiCell):

    name = 'p.pend.n'

    def __init__(self, row, col, strength, temperature=25, moisture=-0.1, wood_strength=1, wood_growth=11.41):
        super().__init__(row, col, strength, wood_strength)

        self.name = 'p.pend.n'

        self.data = total_fungi[self.name]

        self.ref_color = enemy_color[0]
        self.color = (
                    self.ref_color[0],
                    self.ref_color[1],
                    self.ref_color[2],
                    self.strength*1.0
                )


        # self.ref_color = valid_colors[-3]

        # self.moisture = moisture

        self.moisture = round(moisture, 2)
        self.temperature = temperature

        self.base_decomp_rate = self.data['traits']['decomp_rate']
        self.base_growth_rate = self.data['traits']['growth_rate']

        self.avg_density = self.data['traits']['density']
        # Load competitiveness


        self.temperature_growth = self.get_temp_growth(temperature)
        self.moisture_growth = self.data['moisture'][self.data['moisture']['matric_pot']==self.moisture].values[0][2]
        # print("temperature_growth: ", self.temperature_growth)
        # print("moisture_Growth: ", self.moisture_growth)

        self.wood_growth = wood_growth

        # Calculate 
        self.mono_culture_rate = 0
        self.hyphal_growth_rate = 0

        self.comp_rank = self.data['traits']['comp_rank']


class Mtrem(FungiCell):

    name = 'm.trem.n'

    def __init__(self, row, col, strength, temperature=25, moisture=-0.1, wood_strength=1, wood_growth=11.41):

        super().__init__(row, col, strength, wood_strength)
        self.name = 'm.trem.n'

        self.data = total_fungi[self.name]
        self.ref_color = valid_colors[-3]
        self.color = (
                    self.ref_color[0],
                    self.ref_color[1],
                    self.ref_color[2],
                    self.strength*1.0
                )


        # self.moisture = moisture

        self.moisture = round(moisture, 2)
        self.temperature = temperature

        self.base_decomp_rate = self.data['traits']['decomp_rate']
        self.base_growth_rate = self.data['traits']['growth_rate']

        self.avg_density = self.data['traits']['density']
        # Load competitiveness

        self.temperature_growth = self.get_temp_growth(temperature)
        self.moisture_growth = self.data['moisture'][self.data['moisture']['matric_pot']==self.moisture].values[0][2]

        self.wood_growth = wood_growth

        # Calculate 
        self.mono_culture_rate = 0
        self.hyphal_growth_rate = 0


        self.comp_rank = self.data['traits']['comp_rank']

class Tchion(FungiCell):

    name = 't.chion.n'

    def __init__(self, row, col, strength, temperature=25, moisture=-0.1, wood_strength=1, wood_growth=11.41):
        super().__init__(row, col, strength, wood_strength)
        self.name = 't.chion.n'

        self.data = total_fungi[self.name]
        self.ref_color = valid_colors[-3]
        self.color = (
                    self.ref_color[0],
                    self.ref_color[1],
                    self.ref_color[2],
                    self.strength*1.0
                )



        # self.moisture = moisture

        self.moisture = round(moisture, 2)
        self.temperature = temperature

        self.base_decomp_rate = self.data['traits']['decomp_rate']
        self.base_growth_rate = self.data['traits']['growth_rate']

        self.avg_density = self.data['traits']['density']
        # Load competitiveness

        self.temperature_growth = self.get_temp_growth(temperature)
        self.moisture_growth = self.data['moisture'][self.data['moisture']['matric_pot']==self.moisture].values[0][2]

        self.wood_growth = wood_growth

        # Calculate 
        self.mono_culture_rate = 0
        self.hyphal_growth_rate = 0

        self.comp_rank = self.data['traits']['comp_rank']

class Prufa(FungiCell):

    name = 'p.rufa.acer.s'

    def __init__(self, row, col, strength, temperature=25, moisture=-0.1, wood_strength=1, wood_growth=11.41):
        super().__init__(row, col, strength, wood_strength)
        self.name = 'p.rufa.acer.s'
        self.data = total_fungi[self.name]
        self.ref_color = valid_colors[-3]

        self.color = (
                    self.ref_color[0],
                    self.ref_color[1],
                    self.ref_color[2],
                    self.strength*1.0
                )



        # self.moisture = moisture
        self.moisture = round(moisture, 2)
        self.temperature = temperature

        self.base_decomp_rate = self.data['traits']['decomp_rate']
        self.base_growth_rate = self.data['traits']['growth_rate']

        self.avg_density = self.data['traits']['density']
        # Load competitiveness

        self.temperature_growth = self.get_temp_growth(temperature)
        self.moisture_growth = self.data['moisture'][self.data['moisture']['matric_pot']==self.moisture].values[0][2]

        self.wood_growth = wood_growth

        # Calculate 
        self.mono_culture_rate = 0
        self.hyphal_growth_rate = 0

        self.comp_rank = self.data['traits']['comp_rank']
        # print("self.comp_Rank: ", self.comp_rank)
        # exit()


def get_surroundings(cells, row, col):
    """
    Get surrounding cells
    """

    # Left cell
    if col-1 >= 0:
        left_cell = cells[row][col-1]
    else:
        left_cell = None

    # Right cell
    if col+1 < len(cells[row]):
        right_cell = cells[row][col+1]

    else:
        right_cell = None

    # Top cell
    if row-1 >= 0:
        top_cell = cells[row-1][col]
    else:
        top_cell = None

    # bottom cell
    if row+1 < len(cells):
        bottom_cell = cells[row+1][col]
    else:
        bottom_cell = None

    # south-east cell
    if row+1< len(cells) and col+1 < len(cells[row]):
        se_cell = cells[row+1][col+1]
    else:
        se_cell = None

    # south-west cell
    if (row+1< len(cells)) and col-1 >= 0:
        sw_cell = cells[row+1][col-1]

    else:
        sw_cell = None

    # north-east cell
    if row-1 >= 0 and col+1 < len(cells[row]):
        ne_cell = cells[row-1][col+1]
    else:
        ne_cell = None

    # north-west cell
    if row-1 >= 0 and col-1 >= 0:
        nw_cell = cells[row-1][col-1]

    else:
        nw_cell = None

    # current cell
    current_cell = cells[row][col]

    top_neighbor = "{nw_cell} {top_cell} {ne_cell}".format(nw_cell=nw_cell, top_cell=top_cell, ne_cell=ne_cell)
    lr_neighbor = "{left_cell} {current_cell} {right_cell}".format(left_cell=left_cell, current_cell=current_cell, right_cell=right_cell)
    bottom_neighbor = "{sw_cell} {bottom_cell} {se_cell}".format(sw_cell=sw_cell, bottom_cell=bottom_cell, se_cell=se_cell)


    data = {
                'top': top_cell, 'left': left_cell, 'bot': bottom_cell,
                'right': right_cell, 'nw': nw_cell, 'sw': sw_cell, 'ne': ne_cell,
                'se': se_cell, 'current': current_cell
            }

    return data
