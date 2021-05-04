import { ImmerReducer } from 'umi';

export interface GlobalState {
  userName: string;
  userPhone: string;
  room: string;
}

export interface GlobalModelType {
  namespace: 'global';
  state: GlobalState;
  reducers: {
    setUserName: ImmerReducer<GlobalState>;
    setUserPhone: ImmerReducer<GlobalState>;
    setRoom: ImmerReducer<GlobalState>;
  };
}

const GlobalModel: GlobalModelType = {
  namespace: 'global',
  state: { userName: '', userPhone: '', room: '' },
  reducers: {
    setUserName(state, action) {
      state.userName = action.payload;
    },
    setUserPhone(state, action) {
      state.userPhone = action.payload;
    },
    setRoom(state, action) {
      state.room = action.payload;
    },
  },
};

export default GlobalModel;
