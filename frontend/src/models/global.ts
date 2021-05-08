import { ImmerReducer } from 'umi';

export interface GlobalState {
  userName: string;
  userPhone: string;
  userRoom: string;
  isAdmin: boolean;
}

export interface GlobalModelType {
  namespace: 'global';
  state: GlobalState;
  reducers: {
    setUserName: ImmerReducer<GlobalState>;
    setUserPhone: ImmerReducer<GlobalState>;
    setRoom: ImmerReducer<GlobalState>;
    setIsAdmin: ImmerReducer<GlobalState>;
  };
}

const GlobalModel: GlobalModelType = {
  namespace: 'global',
  state: { userName: '', userPhone: '', userRoom: '', isAdmin: false },
  reducers: {
    setUserName(state, action) {
      state.userName = action.payload;
    },
    setUserPhone(state, action) {
      state.userPhone = action.payload;
    },
    setRoom(state, action) {
      state.userRoom = action.payload;
    },
    setIsAdmin(state, action) {
      state.isAdmin = action.payload;
    },
  },
};

export default GlobalModel;
