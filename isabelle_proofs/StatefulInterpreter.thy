theory StatefulInterpreter
  imports Main DataTypes 
begin

record stateful_interpreter =
  public_params :: public_param
  private_params :: private_param
  code :: code
  state :: "(instance_label, instance_state \<times> nat) map" 
  port_count :: nat

definition interpreter_call ::
"'a stateful_interpreter_scheme  \<Rightarrow> functionality_id \<Rightarrow> msg 
\<Rightarrow> (functionality_id \<times> msg) list"  where
"interpreter_call i f m = [(f,m)]"

definition reveal_state ::
"'a stateful_interpreter_scheme \<Rightarrow>(instance_label, instance_state \<times> nat) map \<times> public_param \<times> private_param" where
"reveal_state i = (state i, public_params i, private_params i)"


definition process_inputs ::"'a stateful_interpreter_scheme  \<Rightarrow> nat \<Rightarrow> msg \<Rightarrow> write_instructions"  where
  "process_inputs i input_port msg = 
    if k < 0 or port_count i \<le> input_port
       then ?
     else    "*)
end
