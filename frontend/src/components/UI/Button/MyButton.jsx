import React from "react";

import classes from "./MyButton.module.css";

const MyButton = ({ text, onClick, style, isActive }) => {
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

export default MyButton;
