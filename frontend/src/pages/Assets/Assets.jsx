import React, { useEffect, useState, useRef } from "react";
import { fetchData } from "../../utils/fetchData";
import Loader from "../../components/UI/Loader/Loader";
import classes from "../Page.module.css";
import MyButton from "../../components/UI/Button/MyButton";
import MySubmitButton from "../../components/UI/SubmitButton/MySubmitButton";
import { COLUMNS } from "../../components/UI/Table/Columns";
import { MyTable } from "../../components/UI/Table/MyTable";

const Assets = (keys) => {
    const tab = window.location.pathname.split("/assets/")[1];
    const [data, setData] = useState(null);
    const [values, setValues] = useState();
    const [isVisible, setVisible] = useState(false);
    const [isEditingWithPencil, setIsEditingWithPencil] = useState(false); // Состояние для редактирования карандашом
    const tableRef = useRef(null);
    const fileInputRef = useRef(null);

    useEffect(() => {
        setData(null);
        fetchData("assets", "get", null, (fetchedData) => {
            setData(fetchedData);
        });
    }, [tab]);

    const handleButtonClick = () => {
        fileInputRef.current.click();
    };

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile) {
            const formData = new FormData();
            formData.append("file", selectedFile);
            formData.append("name", tab);

            fetchData(
                `assets/import/`,
                "POST",
                formData,
                () => {
                    fetchData("assets", "get", null, setData);
                },
                setValues,
                setValues
            );
        }
    };

    const handleDownload = () => {
        fetchData(`assets/export?name=${tab}`, "GET", null, null, (error) => console.error("Ошибка запроса:", error), null, true, `${tab}_table.csv`);
    };

    useEffect(() => {
        setVisible(isEditingWithPencil)
    }, [isEditingWithPencil]);
    
    const toggleVisible = () => {
        setVisible(!isVisible);
    };

    const cancelButton = () => {
        const wasEditing = isEditingWithPencil; // Запоминаем состояние перед изменением
    
        if (wasEditing) {
            tableRef.current.cancelEdit(); 
            setTimeout(() => setIsEditingWithPencil(false), 0); 
        } else {
            tableRef.current.addRow(); 
            setIsEditingWithPencil(true); 
        }
    
        toggleVisible();
    };

    const getNestedValue = (obj, path) => {
        if (typeof path !== "string") {
            console.error("keys должен быть строкой, но получен:", path);
            return [];
        }
        return path.split('.').reduce((acc, key) => acc?.[key], obj);
    };
     
    const firstKey = Object.keys(keys)[0];
    const firstValue = keys[firstKey];

    return (
        <div className={classes.main}>
            {data ? (
                <>
                    <MyTable
                        key={`${tab}-${values}`}
                        columnlist={getNestedValue(COLUMNS, firstValue) || []}
                        ref={tableRef}
                        fulldata={data[tab]}
                        onEditingChange={(isEditingWithPencil) => {
                            setIsEditingWithPencil(isEditingWithPencil); // Обновляем состояние
                        }}
                    />
                    <div style={{ display: 'flex' }}>
                        <MyButton
                            style={{ marginTop: '20px', marginRight: '20px', width: '250px' }}
                            onClick={() => {
                                if (isEditingWithPencil) {
                                    tableRef.current?.cancelEdit?.();
                                } else {
                                    tableRef.current?.addRow?.();
                                }
                            }}
                            text={isVisible ? "Отмена" : "Создать запись"}
                        />
                        <MySubmitButton
                            isActive={isVisible}
                            style={{ marginTop: '20px', marginRight: '20px', width: '250px' }}
                            text="Подтвердить" 
                            onClick={() => {
                                tableRef.current.sendData();
                                setVisible(false); // Закрываем кнопку после подтверждения
                                setIsEditingWithPencil(false); // Сбрасываем состояние редактирования
                            }}
                        />
                        <input
                            type="file"
                            ref={fileInputRef}
                            style={{ display: 'none' }}
                            onChange={handleFileChange}
                        />
                        <MyButton
                            style={{ marginTop: '20px', marginLeft: 'auto', width: '250px' }}
                            onClick={handleButtonClick}
                            isActive={false}
                            text={`Импорт ${values ? "values" : ""}`}
                        />
                        <MyButton
                            style={{ marginTop: '20px', marginLeft: '20px', width: '250px' }}
                            onClick={handleDownload}
                            isActive={true}
                            text={'Экспорт'}
                        />
                    </div>
                </>
            ) : (
                <div style={{ margin: "auto" }}>
                    <Loader />
                </div>
            )}
        </div>
    );
};

export default Assets;