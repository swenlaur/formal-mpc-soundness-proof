theory DataTypes
  imports Main
begin

(* Types made up for the project *)
typedecl msg
typedecl party_id 
typedecl functionality_id
typedecl port_no 
type_synonym msg_index = nat
typedecl module_type 
typedecl state 
(* Obviously state can't remain like this. *)

typedecl public_param (* Not sure if they're necessary, still *)
typedecl private_param 

(* Types from the Python code *)
(* code.py *)
typedecl code

(* instance_labels.py *)
typedecl instance_label
typedecl null_instance_label (* constant *)
(* In Python, this inherits from IL *)

(* values.py *)
typedecl value_type
typedecl value_type_label

(* memory_locations.py *)
typedecl memory_location 
typedecl pinned_memory_location (* Constant - option type? *)

(* instance_state.py *)
datatype instance_state = InstanceState "(value_type_label \<Rightarrow> memory_location \<Rightarrow> value_type) option"


(* write_instructions.py *)
datatype write_instructions = WriteInstructions "(port_no \<times> msg) list"

(* trusted_setup.py *)
datatype trusted_setup = TrustedSetup "(public_param \<times> private_param) list"
(* This is supposed to actually be a randomized function. *)
(* Should actually have something more like :
trusted_setup :: random_tape \<Rightarrow> parameter list where
trusted_setup (does something with the random values) *)


(* protocol_description.py *)
datatype protocol_description = ProtocolDescription "code list"
(* similarly here? *)

datatype adv_input =  
  AdvNone |
  CorruptionReply "state \<times> public_param \<times> private_param" |
  PeekReply msg |
  ClockIncomingReply "(port_no, msg) map" |
  SendIncomingReply write_instructions | (* Oh no *)
  InvokeEnvironmentReply msg | (* Any type in Python *)
  QueryFunctionalityReply msg

end