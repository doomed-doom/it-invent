import React, { useState } from "react";
import { fetchData } from "../../utils/fetchData";

import MyInput from "../../components/UI/Input/MyInput";
import MyButton from "../../components/UI/Button/MyButton";

import classes from "../Page.module.css";
import cls from "./Login.module.css";

const Login = () => {
	const [values, setValues] = useState({});

	const handleChange = (event, field) => {
		setValues((prevValues) => ({
			...prevValues,
			[field]: event.target.value,
		}));
	};

	return (
		<div className={cls.login}>
			<div className={classes.fields}>
				<h1 className={classes.title}>Вход</h1>

				<MyInput
					type="text"
					placeholder="Введите логин"
					onChange={(event) => handleChange(event, "username")}
				/>
				<MyInput
					type="password"
					placeholder="Введите пароль"
					onChange={(event) => handleChange(event, "password")}
				/>

				<MyButton
					text="Войти"
					onClick={() => {console.log(values); fetchData("auth/login", "post", values)}}
				/>
			</div>
		</div>
	);
};

export default Login;
