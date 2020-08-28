import React from "react";
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";

import { isAuthenticated } from "./components/services/auth";
import Register from "./components/pages/body/register/register"
import Login from "./components/pages/body/login/login";
import Main from "./components/pages/body/index";

import Faturamento from "./components/pages/body/mainFunction/mainFunction";
import Fechamentos from "./components/pages/body/mainFunction/showBilling";
import ConsumoTotal from "./components/pages/body/mainFunction/showConsumeTotal";

// import Salvar from "./components/pages/body/backup/backupBilling";
// import ASalvar from "./components/pages/body/backup/toBackupBilling";
import Backups from "./components/pages/body/backup/backupDone";

import RegistrarRamais from "./components/pages/body/keepExt/keepExts";
import ManterRamais from "./components/pages/body/keepExt/registerExts";
// import MudarRamaisGrupo from "./components/pages/body/keepExt/changeExtsGroup";
// import DesativarRamais from "./components/pages/body/keepExt/deactivateExts";

import ListarRamais from "./components/pages/body/searchExt/searchExts";
// import ListarRamal from "./components/pages/body/searchExt/searchExt";
import ListarRamaisMes from "./components/pages/body/searchExt/searchExtsMonth";
import ListarRamaisQtde from "./components/pages/body/searchExt/searchExtsQty";


import ManterTipoLigacoes from "./components/pages/body/keepCallType/keepCallTypes";
// import ShowTipoLigacoes from "./components/pages/body/keepCallType/showCallTypes";
// import RemoverTipoLigacoes from "./components/pages/body/keepCallType/deleteCallTypes";

import ManterTarifas from "./components/pages/body/keepFare/keepFares";
import ListarTarifas from "./components/pages/body/keepFare/showFares";
// import AtualizarTarifas from "./components/pages/body/keepFare/updateFares";
// import RemoverTarifas from "./components/pages/body/keepFare/deleteFares";


const PrivateRoute = ({ component: Component, ...rest }) => (
    <Route 
        { ...rest }
        render={ props=>
            isAuthenticated() ? (
                <Component {...props} />
            ) : (
                <Redirect to={{ pathname: "/", state: { from: props.location } }}/>
            )
        }
    />
);

const Routes = () =>(
    <BrowserRouter>
        <Switch>
            <Route exact path="/" component={Login} />
            <Route exact path="/users/register" component={Register} />
            <PrivateRoute exact path="/app" component={Main} />
            <PrivateRoute exact path="/app/faturamento" component={Faturamento} />
            <PrivateRoute exact path="/app/fechamentos" component={Fechamentos} />
            <PrivateRoute exact path="/app/consumoTotal" component={ConsumoTotal}/>
            
            {/* <PrivateRoute exact path="/app/toBackup" component={ASalvar}/>
            <PrivateRoute exact path="/app/backup" component={Salvar} /> */}
            <PrivateRoute exact path="/app/backups" component={Backups}/>
            
            <PrivateRoute exact path="/app/ramais" component={ManterRamais}/>
            <PrivateRoute exact path="/app/manterRamais" component={RegistrarRamais}/>
            {/* <PrivateRoute exact path="/app/mudarRamaisGrupo" component={MudarRamaisGrupo}/>
            <PrivateRoute exact path="/app/desativarRamais" component={DesativarRamais}/> */}
            
            <PrivateRoute exact path="/app/listar" component={ListarRamais}/>
            {/* <PrivateRoute exact path="/app/listarRamal" component={ListarRamal}/> */}
            <PrivateRoute exact path="/app/listarRamaisMes" component={ListarRamaisMes}/>
            <PrivateRoute exact path="/app/listarRamaisQtde" component={ListarRamaisQtde}/>

            <PrivateRoute exact path="/app/tipoLigacoes" component={ManterTipoLigacoes}/>
            {/* <PrivateRoute exact path="/app/showTipoLigacoes" component={ShowTipoLigacoes}/>
            <PrivateRoute exact path="/app/removerTipoLigacoes" component={RemoverTipoLigacoes}/> */}

            <PrivateRoute exact path="/app/tarifas" component={ManterTarifas}/>
            <PrivateRoute exact path="/app/listarTarifas" component={ListarTarifas}/>
            {/* <PrivateRoute exact path="/app/atualizarTarifas" component={AtualizarTarifas}/>
            <PrivateRoute exact path="/app/removerTarifas" component={RemoverTarifas}/> */}

            <Route path="*" component={() => <h1>Page not Found</h1>} />
            {/* <PrivateRoute exact path="/main" component={MainFunction}/> */}
        </Switch>
    </BrowserRouter>
);

export default Routes;