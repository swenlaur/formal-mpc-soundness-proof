theory StatefulInterpreter
  imports 
    Main 
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/data_types/DataTypes"
begin

datatype cmd = Sleep | Eval | Jump | Send | DMACall 
datatype int_msg = Any msg |
 InitMsg "instance_label * instance_label * msg" |
 SleepMsg instance_label

datatype interpreter_instruction =
 NoneInstr | InitInstr | SleepInstr | EvalInstr |
 JumpInstr nat | SendInstr nat | DMAOutInstr nat | DMAInInstr nat

record stateful_interpreter =
  int_public_params :: public_param
  int_private_params :: private_param
  int_program :: "cmd list"
  int_incoming_buffers :: "int_msg list"
  int_outgoing_buffers :: "int_msg list"
  int_count_and_state :: "(instance_label, nat \<times> nat * instance_state) map" 
  int_port_count :: nat


definition get_label :: "int_msg \<Rightarrow> instance_label option" where
"get_label m =
(case m of
Any mm \<Rightarrow> None |
InitMsg (te, t, m) \<Rightarrow> Some t)" 

definition start_counter :: 
"'a stateful_interpreter_scheme \<Rightarrow> instance_label \<Rightarrow> 'a stateful_interpreter_scheme" where
"start_counter s t = 
s\<lparr>int_count_and_state := (int_count_and_state s)(t := Some (1, 0, InstanceState None))\<rparr>"



definition init :: 
"'a stateful_interpreter_scheme \<Rightarrow> ('a stateful_interpreter_scheme option)" where
"init s = 
  (if
  \<exists>te t m. (int_incoming_buffers s) ! 0 = InitMsg (te, t, m) 
  \<and> int_count_and_state s t = None
  then 
    let t = get_label ((int_incoming_buffers s) ! 0) in (map_option (start_counter s) t)
  else None)"

definition set_smth :: 
"'a stateful_interpreter_scheme \<Rightarrow> 'a stateful_interpreter_scheme option" where
"set_smth s = (if \<exists>n. int_port_count s = n 
then let n = int_port_count s in Some (s\<lparr>int_port_count := n + 1\<rparr>) 
else None)"

definition sleep :: 
"'a stateful_interpreter_scheme \<Rightarrow> 'a stateful_interpreter_scheme option" where
"sleep s = 
  (if
  \<exists>t n1 n2 is. (int_count_and_state s) t = Some (n1, n2, is)
  \<and> n2  = 0
  \<and> (int_program s) ! n1 = Sleep
then 
(case  get_label ((int_incoming_buffers s) ! 0) of 
None \<Rightarrow> None |
Some t \<Rightarrow>  Some (s\<lparr>int_outgoing_buffers := SleepMsg t # (int_outgoing_buffers s)\<rparr>))
else None)"


definition eval :: 
"'a stateful_interpreter_scheme \<Rightarrow> 'a stateful_interpreter_scheme option" where
"eval s = (if
  \<exists>t n1 n2 is. (int_count_and_state s) t = Some (n1, n2, is)
  \<and> n2  = 0
  \<and> (int_program s) ! n1 = Eval
then Some s
else None)"


definition jump :: 
"'a stateful_interpreter_scheme \<Rightarrow> 'a stateful_interpreter_scheme option" where
"jump s = (if
True
then Some s
else (if
True 
then Some s
else None))"


(* Tries to do stuff, if fails, goes to next possible do *)
definition do_stuff :: "'a stateful_interpreter_scheme \<Rightarrow> 'a stateful_interpreter_scheme" where
"do_stuff s =
(case init s of 
Some s' \<Rightarrow> s'|
None \<Rightarrow>
(case sleep s of
Some s' \<Rightarrow> s'|
None \<Rightarrow>
(case eval s of 
Some s' \<Rightarrow> s'|
None \<Rightarrow> 
(case jump s of 
Some s' \<Rightarrow> s'|
None \<Rightarrow> s))))"

definition get_write_instructions :: "'a stateful_interpreter_scheme \<Rightarrow> (functionality_id \<times> msg) list" where
"get_write_instructions s = []"

(* Takes the initial state*)
definition interpreter_call ::
"'a stateful_interpreter_scheme  \<Rightarrow> (functionality_id \<times> msg) list"  where
"interpreter_call s = get_write_instructions (do_stuff s)"

(* ============================================================================================== *)

definition reveal_state ::
"'a stateful_interpreter_scheme \<Rightarrow> (instance_label, nat \<times> nat * instance_state) map \<times> public_param \<times> private_param" where
"reveal_state i = (int_count_and_state i, int_public_params i, int_private_params i)"

(* Looks at state of interpreter *)

end
