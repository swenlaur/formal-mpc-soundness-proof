theory StatefulInterpreter
  imports Main DataTypes 
begin

record stateful_interpreter =
  int_public_params :: public_param
  int_private_params :: private_param
  int_code :: code
  int_state :: "(instance_label, instance_state \<times> nat) map" 
  int_port_count :: nat

definition interpreter_call ::
"'a stateful_interpreter_scheme  \<Rightarrow> functionality_id \<Rightarrow> msg 
\<Rightarrow> (functionality_id \<times> msg) list"  where
"interpreter_call i f m = [(f,m)]"

definition reveal_state ::
"'a stateful_interpreter_scheme \<Rightarrow>(instance_label, instance_state \<times> nat) map \<times> public_param \<times> private_param" where
"reveal_state i = (int_state i, int_public_params i, int_private_params i)"

definition process_inputs ::
"'a stateful_interpreter_scheme  \<Rightarrow> nat \<Rightarrow> msg \<Rightarrow> write_instructions"  where
"process_inputs i input_port msg = []"
end
