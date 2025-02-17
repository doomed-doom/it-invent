import React from "react";
import { useNavigate } from "react-router";

import MyButton from "../../components/UI/Button/MyButton";

import classes from "./Error.module.css";

const Error = () => {
	const navigate = useNavigate();

	return (
		<div className={classes.error}>
			<h1>(^-^*)</h1>

			<div className={classes.button}>
				<MyButton text="<- Домой" onClick={() => navigate("/")} />
			</div>
		</div>
	);
};

export default Error;
