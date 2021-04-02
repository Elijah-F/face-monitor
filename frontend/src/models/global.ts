import { ImmerReducer } from 'umi';

export interface GlobalState {
  userName: string;
  userPhone: string;
}

export interface GlobalModelType {
  namespace: 'global';
  state: GlobalState;
  reducers: {
    setUserName: ImmerReducer<GlobalState>;
    setUserPhone: ImmerReducer<GlobalState>;
  };
}

const GlobalModel: GlobalModelType = {
  namespace: 'global',
  state: { userName: '', userPhone: '' },
  reducers: {
    setUserName(state, action) {
      state.userName = action.payload;
    },
    setUserPhone(state, action) {
      state.userPhone = action.payload;
    },
  },
};

export default GlobalModel;
