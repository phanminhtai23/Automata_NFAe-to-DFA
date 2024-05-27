import streamlit as st
import copy
import pandas as pd
from automathon import DFA as DFA_Graph
from automathon import NFA


class DFA:
    def __init__(self):
        self.Q = list()
        self.Σ = list()
        self.Q0 = set()
        self.F = list()
        self.δ = dict()

    def Show_DFA(self):       
        st.write("-----------------------------------Converted DFA-----------------------------------")
        st.write("DFA(Q,Σ,δ,Q0,F)\n")
        
        states_DFA = '{' + ', '.join(self.Q) + '}'
        st.write("Q = ", states_DFA)
            
        boKyHieu = '{' + ', '.join(self.Σ) + '}'
        st.write("Σ =\n    ", boKyHieu)
            
        st.write("δ:")
        
        df = pd.DataFrame(index=self.Q, columns=self.Σ)
        for q in self.Q:
            for i in self.Σ:
                df.loc[q, i] = ', '.join(self.δ.get((q, i), []))
                
        df_styled = df.style.set_table_styles([{'selector': 'th', 'props': [('font-size', '50px')]}])
        st.write(df_styled)

        st.write("Q0:\n    ", self.Q0)
        
        F_DFA = '{' + ', '.join(self.F) + '}'
        st.write("F =\n    ", F_DFA)
            
        
        
    
    def get_states(self):
        return self.Q

    def get_sigma(self):
        return self.Σ

    def get_delta(self):
        delta_dict = {}
        for key, value in self.δ.items():
            state, symbol = key
            if state not in delta_dict:
                delta_dict[state] = {symbol: value}
            else:
                delta_dict[state][symbol] = value
        return delta_dict

    def get_initial_state(self):
        return self.Q0

    def get_final_states(self):
        return self.F

class NFAε:
    def __init__(self):
        self.Q = set()
        self.Σ = list()
        self.δ = dict()
        self.Q0 = None
        self.F = set()

    def Import_file(self, uploaded_file):
        content = uploaded_file.getvalue().decode("utf-8")
        lines = content.split("\n")
        if len(lines[0].split()) == 0:
            raise ValueError(
                "Bạn đã nhập sai định dạng Q0 từ file, vui lòng nhập lại !")
        else:
            self.Q0 = lines[0].split()[0]
        self.F.update(lines[0].split()[1:])
        if len(self.F) == 0:
            raise ValueError(
                "Thiếu trạng thái kết thúc, vui lòng nhập đủ !")
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 3:  # Kiểm tra xem có đủ phần tử trong parts hay không
                self.δ[parts[0], parts[1]] = set(parts[2:])
                self.Q.add(parts[0])
                self.Q.update(parts[2:])
                if parts[1] != 'ε' and parts[1] not in self.Σ:
                    self.Σ.append(parts[1])
            else:
                raise ValueError(
                    "Dữ liệu hàm δ nhập không đúng định dạng, vui lòng kiểm tra lại!")
        
        self.Q = list(self.Q)
        for i in range(0, len(self.Q)):
            self.Q[i] = int(self.Q[i])
        self.Q = sorted(self.Q)
        for i in range(0, len(self.Q)):
            self.Q[i] = str(self.Q[i])
        


    def Import_keyboard(self, Q0_input=None, F_input=None, δ_input=None):

        if Q0_input is not None and Q0_input.strip():
            temp = Q0_input.strip()
            if len(temp) > 1:
                raise ValueError(
                    "Chỉ có một trạng thái đầu, vui lòng kiểm tra lại !")
            else:
                self.Q0 = temp
        else:
            raise ValueError("Trạng thái ban đầu (Q0) không được để trống!")
        self.F.update(F_input.split())
        for line in δ_input.split("\n"):
            parts = line.split()
            if len(parts) >= 3:
                self.δ[parts[0], parts[1]] = set(parts[2:])
                self.Q.add(parts[0])
                self.Q.update(parts[2:])
                if parts[1] != 'ε' and parts[1] not in self.Σ:
                    self.Σ.append(parts[1])
            else:
                raise ValueError(
                    "Dữ liệu hàm δ nhập không đúng định dạng, vui lòng kiểm tra lại!")
        self.Q = list(self.Q)
        for i in range(0, len(self.Q)):
            self.Q[i] = int(self.Q[i])
        self.Q = sorted(self.Q)
        for i in range(0, len(self.Q)):
            self.Q[i] = str(self.Q[i])
            
    def ε_closure(self, States):
        Result = list()
        Queue = list()
        for State in States:
            Queue.append(State)
            Result.append(State)
        while len(Queue) != 0:
            q = Queue.pop(0)
            if (q, 'ε') in self.δ:
                for Value in self.δ[(q, 'ε')]:
                    if Value not in Result:
                        Result.append(Value)
                        Queue.append(Value)
        Result = sorted(Result)
        return Result

    def Move(self, States, c):
        Result = list()
        for q in States:
            if (q, c) in self.δ:
                for Value in self.δ[(q, c)]:
                    Result.append(Value)
                    
        Result = sorted(Result)
        return Result

    def Convert(self):
        
        states = dict()
        char = 'A'
        IsOpen = list()
        Closed = list()
        Result = DFA()
        Start = self.ε_closure({self.Q0})
        IsOpen.append(Start)
        st.write("Chuyển đổi từ NFAε sang DFA\n")
        
        states[tuple(Start)] = char
        
        st.write(
            f"    Trạng thái bắt đầu DFA: \nε_closure({self.Q0}) = {Start} = {char}\n")
        
        ascii_codes = ord(char)
        ascii_codes = int(ascii_codes)+1
        char = chr(ascii_codes)
        # print(char)
        
        while len(IsOpen) > 0:
            q = IsOpen.pop(0)
            Closed.append(q)
            
            for c in self.Σ:
                Next = self.ε_closure(self.Move(q, c))
                if Next not in IsOpen and Next not in Closed and len(Next) != 0:
                    IsOpen.append(Next)
                
                if not (tuple(Next) in states):
                    states[tuple(Next)] = char
                    ascii_codes = ord(char)
                    ascii_codes = int(ascii_codes)+1
                    char = chr(ascii_codes)
                    
                    
                st.write(f"    ε_closure(δ({states[tuple(q)]}, {c})) = ε_closure({self.Move(q, c)}) = {Next} = {states[tuple(Next)]}\n")
                
                if len(Next) != 0:
                    Result.δ[states[tuple(q)], c] = states[tuple(Next)]
        
        for key in states:
            Result.Q.append(states[key])
        Result.Q0 = states[tuple(Start)]
        for State_End in Closed:
            if any(e in State_End for e in self.F):
                Result.F.append(states[tuple(State_End)])
        Result.Σ = copy.deepcopy(self.Σ)
        return Result


    def get_states(self):
        return self.Q

    def get_sigma(self):
        return self.Σ

    def get_delta(self):
        delta_dict = {}
        for key, value in self.δ.items():
            state, symbol = key
            if state not in delta_dict:
                delta_dict[state] = {symbol: value}
            else:
                delta_dict[state][symbol] = value
        return delta_dict

    def get_initial_state(self):
        return self.Q0

    def get_final_states(self):
        return self.F
    
    
    def show_NFAε(self):
        st.write("-----------------------------------Original NFAε-----------------------------------")
        st.write("NFAε(Q,Σ,δ,Q0,F)\n")
        
        q = '{' + ', '.join(self.Q) + '}'
        st.write("Q = ", q)
        
        boKyHieu = '{' + ', '.join(self.Σ) + '}'
        st.write("Σ =\n    ", boKyHieu)
        
        st.write("δ:")
        list_label = self.Σ.copy()
        list_label.append('ε')
        
        df = pd.DataFrame(index=self.Q, columns=list_label)
        
        for q in self.Q:
            for i in list_label:               
                df.loc[q, i] = ', '.join(self.δ.get((q, i), []))
                
        df_styled = df.style.set_table_styles([{'selector': 'th', 'props': [('font-size', '50px')]}])
        st.write(df_styled)
        
        st.write("Q0 =\n    ", self.Q0)
        
        F = '{' + ', '.join(self.F) + '}'
        st.write("F =\n    ", F)

        
        
    
        


def main():
    st.title("==========NFAε to DFA==========")
    st.write("Chọn file NFAε hoặc nhập các thông số từ bàn phím!")

    uploaded_file = st.file_uploader("Hãy chọn file NFAε", type=["txt"])
    Q0_input = st.text_input("Trạng thái ban đầu (Q0):")
    F_input = st.text_input(
        "Các trạng thái kết thúc (F), phân tách bằng dấu cách:")
    δ_input = st.text_area(
        "Chuyển trạng thái (δ), mỗi dòng có dạng: \"trạng thái hiện tại <space> ký hiệu nhập <space> các trạng thái mới\" \n\n vd: 0 ε 1 7, '0' là tt bắt đầu, 'ε' là ký hiệu nhập, '1' và '7' là tt mới")

    convert_button = st.button("Convert")
    if convert_button:
        nfa = NFAε()
        try:
            if uploaded_file is not None:
                nfa.Import_file(uploaded_file)
                nfa.show_NFAε()
                
                q = nfa.get_states()
                sigma = nfa.get_sigma()
                delta =nfa.get_delta()
                initial_state = nfa.get_initial_state()
                f = nfa.get_final_states()
                automata = NFA(q, sigma, delta, initial_state, f)
                automata.view(
                    file_name="NFA_Graph",
                    node_attr={'fontsize': '20'},
                    edge_attr={'fontsize': '20pt'}
                )
                st.subheader("Đồ thị của NFAε")
                st.image("NFA_Graph.gv.png")
                
                dfa = nfa.Convert()
                dfa.Show_DFA()
                q = dfa.get_states()
                sigma = dfa.get_sigma()
                delta =dfa.get_delta()
                initial_state = dfa.get_initial_state()
                f = dfa.get_final_states()
                automata = DFA_Graph(q, sigma, delta, initial_state, f)
                automata.view(
                    file_name="DFA_Graph",
                    node_attr={'fontsize': '20'},
                    edge_attr={'fontsize': '20pt'}
                )
                st.subheader("Đồ thị của DFA")
                st.image("DFA_Graph.gv.png")
            elif Q0_input and F_input and δ_input:
                nfa.Import_keyboard(Q0_input, F_input, δ_input)
                nfa.show_NFAε()
                
                q = nfa.get_states()
                sigma = nfa.get_sigma()
                delta =nfa.get_delta()
                initial_state = nfa.get_initial_state()
                f = nfa.get_final_states()
                automata = NFA(q, sigma, delta, initial_state, f)
                automata.view(
                    file_name="NFA_Graph",
                    node_attr={'fontsize': '20'},
                    edge_attr={'fontsize': '20pt'}
                )
                st.subheader("Đồ thị của NFAε")
                st.image("NFA_Graph.gv.png")
                
                dfa = nfa.Convert()
                dfa.Show_DFA()
                
                q = dfa.get_states()
                sigma = dfa.get_sigma()
                delta =dfa.get_delta()
                initial_state = dfa.get_initial_state()
                f = dfa.get_final_states()
                automata = DFA_Graph(q, sigma, delta, initial_state, f)
                automata.view(
                    file_name="DFA_Graph",
                    node_attr={'fontsize': '20'},
                    edge_attr={'fontsize': '20pt'}
                )
                st.subheader("Đồi thị của DFA")
                st.image("DFA_Graph.gv.png")

            else:
                bug = ''
                if (Q0_input == ''):
                    bug = bug + 'Q0'
                if (F_input == ''):
                    bug = bug + ', F'
                if (δ_input == ''):
                    bug = bug + ', δ'
                print(bug)
                st.warning(f"Vui lòng nhập đủ {bug}!")

        except ValueError as e:
            st.warning(str(e))


if __name__ == "__main__":
    main()
