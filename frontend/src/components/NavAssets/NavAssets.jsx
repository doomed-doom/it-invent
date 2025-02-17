import { useNavigate, useLocation } from "react-router";

import { translateAssets } from "../../utils/assets";

import MyButton from "../../components/UI/Button/MyButton";

import classes from "./NavAssets.module.css";

const NavAssets = ({ tabs }) => {
	const navigate = useNavigate();
	const location = useLocation();

	const isActive = (key) => {
		return location.pathname === `/assets/${key}`;
	};

	return (
		<div className={classes.side}>
			{tabs.map((key) => (
				<MyButton
					key={key}
					text={translateAssets(key)}
					onClick={() => navigate(`/assets/${key}`)}
					isActive={isActive(key)}
				/>
			))}
		</div>
	);
};

export default NavAssets;
