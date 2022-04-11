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
definition env :: environment where
"env =  \<lparr>env_parent_parties = parent_parties, env_outgoing_buffers = [] \<rparr>"
consts ideal_functionalities :: "(functionality_id, standard_functionality) map"
(* Issue w/ modelling env as func: can't distinguish it when inside  a map *)
consts outgoing_signals :: "(party_id * functionality_id * instance_label * instance_label, bool) map"

record  system_state =
  state_protocol_parties ::  "(party_id, protocol_party) map"
  state_env :: environment
  state_ideal_functionalities :: "(functionality_id, standard_functionality) map"
  state_corrupted_parties :: "party_id list"
  state_outgoing_signals :: "(party_id * functionality_id * instance_label * instance_label, bool) map"


record flags =
  is_lazy :: bool
  is_generic :: bool
  is_coherent :: bool
  is_semi_simplistic :: bool



definition system_state_00 where
"system_state_00 = \<lparr>
 state_protocol_parties = protocol_parties,
 state_env = env,
 state_ideal_functionalities = ideal_functionalities,
 state_corrupted_parties = [],
 state_outgoing_signals = outgoing_signals
 \<rparr>"

definition flags_00 where
"flags_00 = \<lparr>
 is_lazy = True,
 is_generic = True,
 is_coherent = True, 
 is_semi_simplistic = True 
\<rparr>"

definition adversary :: lazy_adversary where 
"adversary = \<lparr> public_params = fst parameters_adversary, private_params = snd parameters_adversary\<rparr>"

(* datatype adv_input =  
  AdvNone |
  CorruptionReply "state \<times> public_param \<times> private_param" |
  ClockIncomingReply "(port_no, msg) map" |
  SendIncomingReply write_instructions | (* Oh no *)
  InvokeEnvironmentReply msg | (* Any type in Python *)
  QueryFunctionalityReply msg*) (* Any type in Python, most likely actually Any type (data of modules) *)

(* It currently gives an error, but I have to leave *)
definition small_step :: "system_state \<times> flags \<times> adv_action \<Rightarrow> system_state \<times> flags \<times> adv_input" where
 "small_step (s, f, a) = (case a of
 CorruptParty p \<Rightarrow>
  (case protocol_parties p of
     None \<Rightarrow>
        (s, f, AdvNone) | 
     Some party \<Rightarrow>
        (case corruption_reply party of 
            None \<Rightarrow> 
                (s, f, AdvNone)|
            Some r \<Rightarrow> 
                (s\<lparr>state_corrupted_parties := p # (state_corrupted_parties s)\<rparr>, f, CorruptionReply r))) |
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


(* system_state contains protocol parties and  *)

end
