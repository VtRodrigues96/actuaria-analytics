from sqlalchemy import text

from src.database.connection import get_engine



def get_age_group(age):

    """
    Cria agrupamentos atuariais quinquenais.
    """

    age = int(age)


    if age >= 90:
        return 90, 999


    age_min = (age // 5) * 5

    age_max = age_min + 4


    return age_min, age_max




def build_mortality_age_group():


    engine = get_engine()



    select_query = """

    SELECT

        age,

        sex,

        mortality_rate,

        life_expectancy,

        source


    FROM silver.mortality_clean;

    """



    insert_query = """

    INSERT INTO silver.mortality_age_group

    (

        age_min,

        age_max,

        sex,

        avg_mortality_rate,

        avg_life_expectancy,

        source

    )


    VALUES

    (

        :age_min,

        :age_max,

        :sex,

        :avg_mortality_rate,

        :avg_life_expectancy,

        :source

    )


    ON CONFLICT

    (

        age_min,

        age_max,

        sex

    )


    DO UPDATE SET


        avg_mortality_rate =
            EXCLUDED.avg_mortality_rate,


        avg_life_expectancy =
            EXCLUDED.avg_life_expectancy,


        source =
            EXCLUDED.source;


    """



    with engine.begin() as connection:


        rows = connection.execute(

            text(select_query)

        ).fetchall()



        groups = {}



        for row in rows:


            age_min, age_max = get_age_group(

                row.age

            )


            key = (

                age_min,

                age_max,

                row.sex

            )



            if key not in groups:


                groups[key] = {


                    "mortality_rates": [],


                    "life_expectancies": [],


                    "source": row.source

                }



            groups[key]["mortality_rates"].append(

                float(row.mortality_rate)

            )


            groups[key]["life_expectancies"].append(

                float(row.life_expectancy)

            )



        # =====================================================
        # GARANTE FAIXA ABERTA 90+ PARA OS DOIS SEXOS
        # =====================================================

        for sex in ["M", "F"]:


            key_90_plus = (

                90,

                999,

                sex

            )


            if key_90_plus not in groups:


                available_groups = [

                    key

                    for key in groups.keys()

                    if key[2] == sex

                ]


                if available_groups:


                    last_group = max(

                        available_groups,

                        key=lambda x: x[0]

                    )


                    groups[key_90_plus] = {


                        "mortality_rates":

                            groups[last_group]["mortality_rates"],


                        "life_expectancies":

                            groups[last_group]["life_expectancies"],


                        "source":

                            groups[last_group]["source"]

                    }



        inserted = 0



        for key, values in groups.items():


            age_min, age_max, sex = key



            connection.execute(

                text(insert_query),

                {


                    "age_min": age_min,


                    "age_max": age_max,


                    "sex": sex,


                    "avg_mortality_rate":

                        sum(values["mortality_rates"])

                        /

                        len(values["mortality_rates"]),



                    "avg_life_expectancy":

                        sum(values["life_expectancies"])

                        /

                        len(values["life_expectancies"]),



                    "source":

                        values["source"]

                }

            )


            inserted += 1



    print(

        f"Faixas etárias criadas: {inserted}"

    )




if __name__ == "__main__":


    build_mortality_age_group()