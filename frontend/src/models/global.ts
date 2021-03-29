import { ImmerReducer } from 'umi';

export interface GlobalState {
  userName: string;
}

export interface GlobalModelType {
  namespace: 'global';
  state: GlobalState;
  reducers: {
    setUserName: ImmerReducer<GlobalState>;
  };
}

const GlobalModel: GlobalModelType = {
  namespace: 'global',
  state: { userName: '' },
  reducers: {
    setUserName(state, action) {
      state.userName = action.payload;
    },
  },
};

export default GlobalModel;
