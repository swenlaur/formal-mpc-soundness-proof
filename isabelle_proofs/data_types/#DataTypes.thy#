theory DataTypes
  imports 
    Main 
begin

typedecl payload 
datatype msg = Message "nat * nat * payload"
type_synonym party_id = nat
type_synonym functionality_id = nat
type_synonym msg_index = nat
typedecl module_type 

typedecl public_param
typedecl private_param 
typedecl instance_label
typedecl null_instance_label
typedecl value_type
typedecl value_type_label

(* memory_locations.py *)
typedecl memory_location 
typedecl pinned_memory_location
datatype instance_state = InstanceState "(value_type_label \<Rightarrow> memory_location \<Rightarrow> value_type) option"
datatype trusted_setup = TrustedSetup "(public_param \<times> private_param) list"
(* This is supposed to actually be a randomized function. *)
(* Should actually have something more like :
trusted_setup :: random_tape \<Rightarrow> parameter list where
trusted_setup (does something with the random values) *)


(* protocol_description.py *)
datatype cmd = Sleep | Eval | Jump | Send | DMACall 
datatype int_msg = Any msg |
 InitMsg "instance_label * instance_label * msg" |
 SleepMsg instance_label

typedecl function_name

datatype interpreter_instruction =
 NoneInstr | InitInstr | SleepInstr | EvalInstr |
 JumpInstr nat | SendInstr nat | DMAOutInstr nat | DMAInInstr nat

datatype protocol_description = ProtocolDescription "cmd list list"
(* similarly here? *)

type_synonym write_instructions = "(nat \<times> msg) list"
consts get_protocol_instances :: "msg \<Rightarrow> instance_label \<times> instance_label"

datatype adv_input =  
  AdvNone |             
  CorruptionReply "(instance_label, instance_state \<times> nat) map \<times> public_param \<times> private_param" |
  PeekReply msg |
  ClockIncomingReply "(nat \<times> msg) option" |
  SendIncomingReply write_instructions |
  QueryFunctionalityReply "msg * write_instructions" (* Any type in Python *)
end