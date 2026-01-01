from create_kitchen import create_kitchens_from_excel
from create_category import create_categories_from_excel
from extra_notes import create_extra_notes_from_excel
from add_ons import create_addons_from_excel
from create_item import create_items_from_excel

EXCEL_FILE = "data.xlsx"

def main():
    print("\n🚀 STARTING FULL FOODIEE SETUP\n")

    print("🍳 Creating kitchens...")
    create_kitchens_from_excel(EXCEL_FILE)

    print("📂 Creating categories...")
    create_categories_from_excel(EXCEL_FILE)

    print("📝 Creating extra notes...")
    create_extra_notes_from_excel(EXCEL_FILE)

    print("➕ Creating addons...")
    create_addons_from_excel(EXCEL_FILE)

    print("🍽️ Creating food items...")
    create_items_from_excel(EXCEL_FILE)

    print("\n🎉 ALL SETUP COMPLETED SUCCESSFULLY 🎉")


if __name__ == "__main__":
    main()
