theory CompleteExecution00
  imports Main DataTypes
    AdversarialAction ProtocolParty ParentParty StandardFunctionality LazyAdversary Environment
begin

definition n :: nat where "n = 2"
definition k :: nat where "k = 2" 

consts parameters_parties :: "(party_id, public_param \<times> private_param) map"
consts parameters_functionalities :: "(functionality_id, public_param \<times> private_param) map"
consts parameters_adversary :: "public_param \<times> private_param"

(* NB. Not modelling a randomized algorithm. *)
consts protocol_description :: "(party_id, code) map"

consts parent_parties :: "(party_id, parent_party) map"
consts protocol_parties :: "(party_id, protocol_party) map"
(* A whole passage building up the parent_parties, the protocol_parties maps, *)
(* the environment, and the ideal functionalities. *)
(* Should I actually initialize these? *)

definition env :: environment where
"env =  \<lparr>env_parent_parties = parent_parties, env_outgoing_buffers = [] \<rparr>"

consts ideal_functionalities :: "(functionality_id, standard_functionality) map"

definition adversary :: lazy_adversary where 
"adversary = \<lparr> public_params = fst parameters_adversary, private_params = snd parameters_adversary\<rparr>"

(* datatype adv_input =  
  AdvNone |
  CorruptionReply "state \<times> public_param \<times> private_param" |
  ClockIncomingReply "(port_no, msg) map" |
  SendIncomingReply write_instructions | (* Oh no *)
  InvokeEnvironmentReply msg | (* Any type in Python *)
  QueryFunctionalityReply msg*) (* Any type in Python, most likely actually Any type (data of modules) *)

definition action_to_input :: "adv_action \<Rightarrow> adv_input" where
 
 "action_to_input a = (case a of

    CorruptParty p \<Rightarrow> (case protocol_parties p of
      None \<Rightarrow> AdvNone | 
      Some party \<Rightarrow> (case corruption_reply party of 
        None \<Rightarrow> AdvNone|
        Some r \<Rightarrow> CorruptionReply r)) |

    BufferAction b \<Rightarrow> (case bufferAction b of 
      Clock \<Rightarrow> (case bufferDirection b of
        Incoming \<Rightarrow> AdvNone|
        Outgoing \<Rightarrow> AdvNone ) |
      Send \<Rightarrow> (case bufferDirection b of
        Incoming \<Rightarrow> AdvNone|
        Outgoing \<Rightarrow> AdvNone )) |

    InvokeEnvironment m \<Rightarrow> InvokeEnvironmentReply (env_adv_probe env m) |

    QueryFunctionality q \<Rightarrow> (case ideal_functionalities (queryTarget q) of
      None \<Rightarrow> AdvNone |
      Some fnl \<Rightarrow> QueryFunctionalityReply (fnl_adv_probe fnl (queryMessage q))))"


consts input_to_action ::  "adv_input \<Rightarrow> adv_action"
definition next_action :: "adv_action \<Rightarrow> adv_action"  where
"next_action action = input_to_action (action_to_input action)"




end