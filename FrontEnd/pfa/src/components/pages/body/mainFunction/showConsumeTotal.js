import React, { Component } from "react";
import Menu from "../../menu/menu";
import Select from 'react-select';
import Data from "../../../services/api";
import Currency from 'react-currency-format';

// import moment from 'moment';


export default class showConsumeTotal extends Component {
    constructor() {
        super();
        this.state = {
            year: null,
            month: null,
            selectedYear: new Date().getFullYear(),
            selectedMonth: parseInt(new Date().getMonth()) + 1,
            total: 0,
            total_ext: 0,
            total_llm: 0,
            total_exc: 0,
            total_min: 0,
            total_ldn_min: 0,
            total_local_min: 0,
            total_movel_min: 0,
            content: [],
            info: []
        }
    }
    componentDidMount() {
        this.loadYearMonth();

        // this.total();
    }

    loadYearMonth = async () => {
        let ano = [];
        let mes = [];
        // const { selectedYear, year } = this.state;
        const resp_Y = await Data.get(`/ano`);
        const resp_M = await Data.get(`/mes`);
        ano = resp_Y.data.map((id_ano) => { return { value: id_ano.id_ano, label: id_ano.id_ano } });
        mes = resp_M.data.map((id_mes) => { return { value: id_mes.id_mes, label: id_mes.mes } });
        // console.log("Years", ano);
        this.setState({ year: ano, month: mes });
    }
    // Year Selected
    yearChange = selectedYear => {
        this.setState({ selectedYear });
        // console.log(`Year Selected: `, selectedYear.value);
    };
    // Month Selected
    monthChange = selectedMonth => {
        this.setState({ selectedMonth });
        // console.log(`Month Selected: `, selectedMonth.value);
    };

    handleSubmit = async e => {
        const { selectedYear, selectedMonth } = this.state;

        const response = await Data.get(`/pmpg/total/${selectedYear.value}${selectedMonth.value}`);
        const { data } = response;
        // console.log("Data", data)
        this.setState({ content: data });
        // console.log(this.state.content);
        this.total();
        this.mapping();
    }

    mapping = () => {
        // console.log("Content", this.state);
        const response = (this.state.content.map((info) => (
            <article className="sec" key={info.id}>
                <div className="header">
                    <h5>{info.group}</h5>
                    <ul className="lst">
                        <li>Serviços: STFC</li>
                        <li>Ramais: {info.ramal_ativo}</li>
                        <li>Total Ramais: {this.mask(info.faturar_ramais, ",", "R$ ", ".")}</li>
                        <li>Total Serviço: {this.mask(info.total_faturar, ",", "R$ ", ".")}</li>
                    </ul>
                </div>
                <hr />
                <div className="plan">
                    <table className="tbl">
                        <thead className="hd">
                            <tr>
                                <td colSpan="5">Franquias/Excedentes</td>
                            </tr>
                            <tr>
                                <th></th>
                                <th>Minutos</th>
                                <th>Valores</th>
                                <th>Minutos Excedentes</th>
                                <th>Valores Excedentes</th>
                            </tr>
                        </thead>
                        <tbody className="bodyT">
                            <tr>
                                <td>Local</td>
                                <td>{this.mask(info.local_minutes, ":", " ")}</td>
                                <td>{this.mask(info.local_values, ",", "R$ ", ".")}</td>
                                <td>{this.mask(info.local_minutes_exc, ":", " ")}</td>
                                <td>{this.mask(info.local_values_exc, ",", "R$ ", ".")}</td>

                            </tr>
                            <tr>
                                <td>LDN</td>
                                <td>{this.mask(info.ldn_minutes, ":", " ")}</td>
                                <td>{this.mask(info.ldn_values, ",", "R$ ", ".")}</td>
                                <td>{this.mask(info.ldn_minutes_exc, ":", " ")}</td>
                                <td>{this.mask(info.ldn_values_exc, ",", "R$ ", ".")}</td>
                            </tr>
                            <tr>
                                <td>Móvel</td>
                                <td>{this.mask(info.movel_minutes, ":", " ")}</td>
                                <td>{this.mask(info.movel_values, ",", "R$ ", ".")}</td>
                                <td>{this.mask(info.movel_minutes_exc, ":", " ")}</td>
                                <td>{this.mask(info.movel_values_exc, ",", "R$ ", ".")}</td>
                            </tr>
                            <tr>
                                <td>Total</td>
                                <td>{this.mask(info.local_minutes
                                    + info.ldn_minutes
                                    + info.movel_minutes, ":", " ")}</td>
                                <td>{this.mask(info.local_values
                                    + info.ldn_values
                                    + info.movel_values, ",", "R$ ", ".")}</td>
                                <td>{this.mask(this.secToTime(
                                    this.minutes(info.local_minutes_exc)
                                    + this.minutes(info.ldn_minutes_exc)
                                    + this.minutes(info.movel_minutes_exc)), ":", " ")}</td>
                                <td>{this.mask(info.local_values_exc
                                    + info.ldn_values_exc
                                    + info.movel_values_exc, ",", "R$ ", ".")}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </article>
        )))

        this.setState({ info: response })
    }

    secToTime = (time) => {
        // recebe o tempo em segundos e depois converto para minutos com o mod
        // concatenando no final
        const min = Math.floor(time / 60);
        const sec = time - min * 60;
        const result = String(min).concat(':', sec)

        return result
    }

    minutes = (time) => {

        const part = (String(time === 0 ? "0.00" : time.toFixed(2))).split('.')
        const min = isNaN(part[0]) ? 0 : parseFloat(part[0]);
        const sec = isNaN(part[1]) ? 0 : parseFloat(part[1]);
        // Isolo e nivelo os minutos para segundos e realizo a soma com os minutos
        const total_sec = (parseInt(min) === 0 ? 0 : (parseInt(min) * 60)) + ((parseInt(sec)) === 0 ? 0 : (parseInt(sec)))
        // retorno todos tudo em segundo
        return total_sec
    }

    mask = (Value, Decimal, Prefix, TS) => {
        const valor = (<Currency displayType={'text'}
            value={Value}
            thousandSeparator={TS}
            decimalSeparator={Decimal}
            prefix={Prefix}
            decimalScale={2}
            fixedDecimalScale={true} />)
        return valor
    }

    total = () => {
        const { content } = this.state;
        const total_geral = (content.map((ttl) => (ttl.total_faturar)).reduce((tt, next) => (tt + next)))
        const total_ext = (content.map((ttl) => (ttl.faturar_ramais)).reduce((tt, next) => (tt + next)))
        const total_llm = (content.map((ttl) => (ttl.local_values
            + ttl.ldn_values
            + ttl.movel_values)).reduce((tt, next) => (tt + next)))
        const total_exc = (content.map((ttl) => (ttl.local_values_exc
            + ttl.ldn_values_exc
            + ttl.movel_values_exc))).reduce((tt, next) => (tt + next))
        const total_ldn_min = (content.map((ttl) => (this.minutes(parseFloat(ttl.ldn_minutes_exc))))).reduce((tt, next) => (tt + next))
        const total_local_min = (content.map((ttl) => (this.minutes(parseFloat(ttl.local_minutes_exc))))).reduce((tt, next) => (tt + next))
        const total_movel_min = (content.map((ttl) => (this.minutes(parseFloat(ttl.movel_minutes_exc))))).reduce((tt, next) => (tt + next))

        this.setState({
            total: total_geral
            , total_ext: total_ext
            , total_llm: total_llm
            , total_exc: total_exc
            , total_ldn_min
            , total_local_min
            , total_movel_min
        })
    }


    render() {
        const { selectedYear, selectedMonth, info, year, month, total, total_ext, total_llm, total_exc, total_ldn_min, total_local_min, total_movel_min } = this.state;
        // console.log("Info", info)
        return (
            <div className="mainDiv">
                <div className="menu">
                    <Menu />
                </div>
                <h1>Pesquisar Faturamento - Consumo Total</h1>
                <div className="finders">
                    <Select
                        className="selected"
                        value={selectedYear}
                        onChange={this.yearChange}
                        options={year}
                        placeholder="Selecione o Ano"
                        isSearchable />

                    <Select
                        className="selected"
                        value={selectedMonth}
                        onChange={this.monthChange}
                        options={month}
                        placeholder="Selecione o Mês"
                        isSearchable />
                    <button className="findButton" onClick={this.handleSubmit}>Pesquisar</button>
                </div>
                <div>
                    <div className="total">
                        <h1>Total Geral</h1>
                        <p>Total Serviços:{this.mask(total, ",", "R$ ", ".")}</p>
                        <p className="ttl">Total Ramais: {this.mask(total_ext, ",", "R$ ", ".")}</p>
                        <p className="ttl">Total Franquias: {this.mask(total_llm, ",", "R$ ", ".")}</p>
                        <p className="ttl">Total Excedentes: {this.mask(total_exc, ",", "R$ ", ".")}</p>
                        <p className="ttl">Total Minutos: {this.mask(this.secToTime(total_ldn_min + total_local_min + total_movel_min), ":", " ")}</p>
                    </div>
                </div>
                <div className="flex">
                    {info}
                </div>
            </div>

        )
    }
}