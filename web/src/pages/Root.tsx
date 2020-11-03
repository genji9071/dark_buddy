import React, { Suspense } from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import Result from './Result';
import Darkspy from "./Darkspy";
import { ROOT_PATH } from 'config';

export default () => {
  return (
    <Suspense fallback>
      <BrowserRouter>
        <Switch>
          <Route path={`${ROOT_PATH}/result`} component={Result} />
          <Route path={`${ROOT_PATH}/darkspy/getword`} component={Darkspy} />
        </Switch>
      </BrowserRouter>
    </Suspense>
  );
}