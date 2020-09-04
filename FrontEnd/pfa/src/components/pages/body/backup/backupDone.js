import React, { Component } from "react";
import Menu from "../../menu/menu";
import Select from 'react-select';
import api from "../../../services/api";
import { checkArray } from '../../../utils/bytes';
import '../index.css';


export default class backupDone extends Component {
    constructor() {
        super();
        this.state = {
            contentData: [],
            periodSelected: null,
            backup: [],
            period: [],
        }
    }

    componentDidMount = async () => {
        this.backupDone();
        this.toBackup();
    }

    backupDone = async (page = 1) => {
        const response = await api.get(`/backupDone/${page}`);
        // console.log(response);
        const { Data } = response.data;
        this.setState({ contentData: Data });
    }

    toBackup = async () => {
        let my = [];
        const response = await api.get(`/backup`);
        const { data } = response;
        my = data.map((dt) => { return { value: dt.MES_ID, label: dt.MES_ID } })
        this.setState({ backup: data, period: my });
    }

    periodChange = periodSelected => {
        this.setState({ periodSelected });
        console.log(`Período Selected: `, periodSelected.value);
    };

    handleSubmit = async e => {
        const { periodSelected } = this.state;
        try{
            // console.log('period',periodSelected.value);
            checkArray(periodSelected);
            await api.get(`/backup/${periodSelected.value}`);
        } catch(err){
            console.log(err);
            return alert('Não há backups para serem realizados')
        }
        this.setState(({periodSelected: null}));
        this.backupDone();
        this.toBackup();
    }

    render() {
        const { contentData, backup, period, periodSelected } = this.state;

        return (
            <div className="mainDiv">
                <div className="menu">
                    <Menu />
                </div>
                <h1>Backups de Faturamentos Realizados</h1>
                <div className="group">
                    <div className="backup">
                        <table>
                            <thead>
                                <tr>
                                    <th>Data de Criação</th>
                                    <th>Fechamento Criado</th>
                                    <th>Quantidade de CDR's</th>
                                    <th>Schema</th>
                                </tr>
                            </thead>
                            {contentData.map(data => (
                                <tbody key={data.table_name}>
                                    <tr>
                                        <td>{data.create_time}</td>
                                        <td>{data.table_name}</td>
                                        <td>{data.table_rows}</td>
                                        <td>{data.table_schema}</td>
                                    </tr>
                                </tbody>
                            ))}
                        </table>
                    </div>
                    <div className="doBackup">
                        <h2>Período para Backup</h2>
                        <div className="finders">
                            <Select
                                className="selected"
                                value={periodSelected}
                                onChange={this.periodChange}
                                options={period}
                                placeholder="Selecione o Período"
                                isSearchable />
                            <button className="doBackup" onClick={this.handleSubmit}>Backup</button>
                        </div>
                    </div>
                    <div className="toBackup">
                    <h2>Backups Pendentes</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>Ano-Mês</th>
                                    <th>Quantidade de CDR's</th>
                                </tr>
                            </thead>
                            {backup.map(data => (
                                <tbody key={data.MES_ID}>
                                    <tr>
                                        <td>{data.MES_ID}</td>
                                        <td>{data.QTY}</td>
                                    </tr>
                                </tbody>
                            ))}
                        </table>
                    </div>
                </div>
            </div>

        )
    }
}