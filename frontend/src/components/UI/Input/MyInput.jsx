import React from "react";

import classes from "./MyInput.module.css";

const MyInput = ({ onChange, type, placeholder }) => {
	return (
		<input
			className={classes.input}
			onChange={onChange}
			type={type}
			placeholder={placeholder}
		/>
	);
};

export default MyInput;
