import React from "react";

import classes from "./MySubmitButton.module.css";

const MySubmitButton = ({ text, onClick, style, isActive }) => {
	return (
		<button
			className={`${classes.button} ${isActive && classes.active}`}
			onClick={onClick}
			style={style}
		>
			{text}
		</button>
	);
};

export default MySubmitButton;
