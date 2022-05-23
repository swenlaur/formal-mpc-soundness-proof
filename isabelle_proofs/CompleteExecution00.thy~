theory CompleteExecution00
  imports Main DataTypes
    AdversarialAction ProtocolParty
    Buffers ParentParty StandardFunctionality 
    LazyAdversary Environment Utils
begin

definition n :: nat where "n = 2"
definition k :: nat where "k = 2" 
consts protocol_description :: "(party_id, code) map"


consts parameters_parties :: "(party_id, public_param \<times> private_param) map"
consts parameters_functionalities :: "(functionality_id, public_param \<times> private_param) map"
consts parameters_adversary :: "public_param \<times> private_param"

consts protocol_parties :: "(party_id, protocol_party) map"
definition env :: environment where
"env =  \<lparr> env_outgoing_buffers = [] \<rparr>"
consts ideal_functionalities :: "(functionality_id, standard_functionality) map"

(* No more *)
consts outgoing_signals :: "(party_id \<times> functionality_id * instance_label * instance_label, bool) map"


record  system_state =
  state_protocol_parties ::  "(party_id, protocol_party) map"
  state_env :: environment
  state_ideal_functionalities :: "(functionality_id, standard_functionality) map"
  state_corrupted_parties :: "party_id set"
  state_outgoing_signals :: "(party_id * functionality_id * instance_label * instance_label, bool) map"
  state_previous_action :: adv_action
  state_flag :: bool


definition system_state_00 where
"system_state_00 = \<lparr>
 state_protocol_parties = protocol_parties,
 state_env = env,
 state_ideal_functionalities = ideal_functionalities,
 state_corrupted_parties = {},
 state_outgoing_signals = outgoing_signals,
 state_previous_action = Empty,
 state_flag = True
 \<rparr>"

definition adversary :: lazy_adversary where 
"adversary = \<lparr>
 public_params = fst parameters_adversary, 
private_params = snd parameters_adversary
\<rparr>"



consts repack_write_instr ::
"party_id \<Rightarrow> (functionality_id \<times> msg) list \<Rightarrow> ((party_id \<times> functionality_id) \<times> msg) list"


(* YIKES! *)

(*Adversarial Input Cheat Sheet:

 datatype adv_input =
  AdvNone |
  CorruptionReply "state \<times> public_param \<times> private_param" |
  PeekReply msg |
  ClockIncomingReply "(port_no, msg) map" |
  SendIncomingReply write_instructions | (* Oh no *)
  InvokeEnvironmentReply msg | (* Any type in Python *)
  QueryFunctionalityReply msg (* Any type in Python, most likely actually Any type (data of modules) *)
*) 


(* WIP:

Halfway through ClockIncomingBuffer.

Refactoring the code such that buffers are entirely consumed by protocol parties. That is, 
there's no separate Buffer datatype.

Refactored the function to be f : S x A \<rightarrow> S x I.

 *)

fun adv_step ::
 "system_state  \<times> adv_action \<Rightarrow> system_state \<times> adv_input" where
"adv_step (s, action)  = 
(case action of
  Empty \<Rightarrow> (s, AdvNone) |
 
  CorruptParty p \<Rightarrow>
  (case protocol_parties p of
     None \<Rightarrow>
        (s, AdvNone) |
     Some party \<Rightarrow>
        if party \<in> state_corrupted_parties s then (s, AdvNone) else 
        (s\<lparr>state_corrupted_parties := insert party (state_corrupted_parties s),
           state_previous_action := CorruptParty p\<rparr>,
         CorruptionReply (internal_state party))) |
  
  BufferAction b \<Rightarrow>
  (case bufferAction b of
 
      Peek \<Rightarrow>
      (case bufferDirection b of
        Incoming \<Rightarrow>
        (case incoming_buffers (bufferParty b, bufferFunc b) of
            None \<Rightarrow> (s, AdvNone) |
            Some lb \<Rightarrow>
                (s, PeekReply (peek_message lb (bufferInd b))))|

        Outgoing \<Rightarrow> 
        (case outgoing_buffers (bufferParty b, bufferFunc b) of
            None \<Rightarrow> (s, AdvNone) |
            Some lb \<Rightarrow>
                (s, PeekReply (peek_message lb (bufferInd b)))))|

      Clock \<Rightarrow>
      (case bufferDirection b of

        Incoming \<Rightarrow> 
        (let s = (if (\<exists>p.\<exists>func. p \<in>(state_corrupted_parties s)
                        \<and> func \<in> (dom (state_ideal_functionalities s))
                        \<and> empty (state_incoming_buffers s (p, func))) 
          then s\<lparr>state_flag := False\<rparr> else s) in
        (case incoming_buffers (bufferParty b, bufferFunc b) of
            None \<Rightarrow> (s, AdvNone) |
            Some lb \<Rightarrow>
                (let m = clock_message lb (bufferInd b) in
                (case protocol_parties (bufferParty b) of
                  None \<Rightarrow> (s, AdvNone) |
                  Some party \<Rightarrow> (s, AdvNone)))))|

        Outgoing \<Rightarrow> (s, AdvNone))) |

  SendMessage send \<Rightarrow> (s, AdvNone)|
  InvokeEnvironment m \<Rightarrow> (s, InvokeEnvironmentReply (env_adv_probe env m)) |
  QueryFunctionality q \<Rightarrow> (case ideal_functionalities (queryTarget q) of
      None \<Rightarrow>  (s, AdvNone) |
      Some fnl \<Rightarrow> (s, QueryFunctionalityReply (fnl_adv_probe fnl (queryMessage q)))))"




end
