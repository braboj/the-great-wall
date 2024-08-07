from proof_of_concept import WallSection, WallProfile, WallBuilder


def test_section():

    # Create a wall section with a start height of 1 foot
    section = WallSection(start_height=1)

    # Simulate building the wall section by one foot per day
    for i in range(30):
        print(section.build())


def test_profile():

    # Create a wall profile with 3 sections
    sections = [WallSection(start_height=i) for i in range(1, 4)]
    profile = WallProfile(full_name="Profile 1", sections=sections)

    for day in range(30):
        print(f"Day {day + 1}")
        for section in profile.sections:
            print(section.build())

    print('-' * 80)
    print(f'TOTAL ICE : {profile.get_ice()}')
    print(f'TOTAL COST: {profile.get_cost()}')


if __name__ == "__main__":
    # test_section()
    test_profile()