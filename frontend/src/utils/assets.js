export const translateAssets = (text) => {
	switch (text) {
		case "components":
			return "Комплектующие";
		case "consumables":
			return "Расходники";
		case "equipments":
			return "Оборудование";
		case "movements":
			return "Перемещения";
		case "programs":
			return "Программы";
		case "repairs":
			return "Ремонт";
		default:
			return text;
	}
};
