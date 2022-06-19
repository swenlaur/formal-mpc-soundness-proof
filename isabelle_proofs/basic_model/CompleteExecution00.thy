theory CompleteExecution00
  imports 
    Main 
    AdversarialAction 
    ProtocolParty
    StandardFunctionality
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/data_types/DataTypes"
    "~/IsabelleProjects/formal-mpc-soundness-proof/isabelle_proofs/network_components/Environment"
begin

definition n :: nat where "n = 2"
definition k :: nat where "k = 2" 
consts protocol_description :: "(party_id, code) map"

consts get_protocol_instances :: "msg \<Rightarrow> instance_label \<times> instance_label"

consts parameters_parties :: "(party_id, public_param \<times> private_param) map"
consts parameters_functionalities :: "(functionality_id, public_param \<times> private_param) map"
consts parameters_adversary :: "public_param \<times> private_param"

consts protocol_parties :: "(party_id, protocol_party) map"
definition env :: environment where
"env =  \<lparr> env_outgoing_buffers = [] \<rparr>"
consts ideal_functionalities :: "(functionality_id, standard_functionality) map"

consts outgoing_signals :: "(party_id \<times> functionality_id * instance_label * instance_label, bool) map"

(* Define and instantiate a system state *)
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


consts repack_write_instr ::
"party_id \<Rightarrow> (functionality_id \<times> msg) list \<Rightarrow> ((party_id \<times> functionality_id) \<times> msg) list"

(*
Adversarial Input Cheat Sheet:

datatype adv_input =  
  AdvNone |
  CorruptionReply "state \<times> public_param \<times> private_param" |
  PeekReply msg |
  ClockIncomingReply "(functionality_id \<times> msg) option" |
  SendIncomingReply "(functionality_id \<times> msg) list" | (* Oh no *)
  InvokeEnvironmentReply msg | (* Any type in Python *)
  QueryFunctionalityReply msg

*) 

(* TODO: add Clock \<rightarrow> Send laziness test. *)
fun no_action :: "system_state \<Rightarrow> system_state * adv_input" where
"no_action s = (s, AdvNone)"


fun adv_corrupt_party :: "system_state \<Rightarrow> party_id \<Rightarrow> protocol_party \<Rightarrow> system_state * adv_input" where
"adv_corrupt_party s p party = 

  (s\<lparr>state_corrupted_parties := insert p (state_corrupted_parties s),
  state_protocol_parties := (state_protocol_parties s) (p := Some (corrupt_party party)),
  state_previous_action := CorruptParty p\<rparr>,

  AdvNone)"


fun adv_peek_incoming_buffer :: "system_state \<Rightarrow> buffer_action \<Rightarrow> protocol_party \<Rightarrow> system_state * adv_input" where
"adv_peek_incoming_buffer s b party = 
(case peek_incoming_buffer party (bufferFunc b) (bufferInd b) of
None \<Rightarrow> no_action s |
Some m \<Rightarrow> (s\<lparr>state_previous_action := BufferAction b\<rparr>, PeekReply m))"


fun adv_peek_outgoing_buffer :: "system_state \<Rightarrow> buffer_action \<Rightarrow> protocol_party \<Rightarrow> system_state * adv_input" where
"adv_peek_outgoing_buffer s b party = 
(case peek_outgoing_buffer party (bufferFunc b) (bufferInd b) of
None \<Rightarrow> no_action s|
Some m \<Rightarrow> (s\<lparr>state_previous_action := BufferAction b\<rparr>, PeekReply m))"


fun adv_clock_incoming_buffer :: "system_state \<Rightarrow> buffer_action \<Rightarrow> protocol_party \<Rightarrow> system_state * adv_input" where
"adv_clock_incoming_buffer s b party = 
(let s0 = (if (\<exists>p.\<exists>func. 
          state_protocol_parties s p = Some party
        \<and> is_corrupted party
        \<and> \<not>(empty_incoming_buffer party func)) 
           then s\<lparr>state_flag := False\<rparr>
           else s) in
(let (opt_m, p) = (clock_message party (bufferFunc b) (bufferInd b)) in
(case opt_m of 
None \<Rightarrow> (s, AdvNone) |
Some m \<Rightarrow>
(let (write_instructions, reply) = party_call party (bufferFunc b) m in
(case reply of
None \<Rightarrow> 
(s0\<lparr>state_protocol_parties := 
            map_upds (state_protocol_parties s) 
                   [bufferParty b] 
                   [do_write_instructions party write_instructions],
   state_previous_action := BufferAction b\<rparr>,
ClockIncomingReply reply) |
Some r \<Rightarrow> 
(s0\<lparr>state_previous_action := BufferAction b\<rparr>, ClockIncomingReply reply))))))"

fun adv_clock_outgoing_buffer :: "system_state \<Rightarrow> buffer_action \<Rightarrow> protocol_party \<Rightarrow> system_state * adv_input" where
"adv_clock_outgoing_buffer s b party = 
(case (state_ideal_functionalities s) (bufferFunc b) of
None \<Rightarrow> (s, AdvNone) |
Some func \<Rightarrow>
(let (opt_m, p) = (clock_message party (bufferFunc b) (bufferInd b)) in
(case opt_m of 
None \<Rightarrow> (s, AdvNone) |
Some m \<Rightarrow> 
(let (t1, t2) = get_protocol_instances m in
(let flag_1 =  (if (\<exists>p.\<exists>func. 
          state_protocol_parties s p = Some party
        \<and> is_corrupted party
        \<and> \<not>(empty_incoming_buffer party func)) 
then False else True) in
(let new_func_map = map_upds (state_ideal_functionalities s) 
                             [bufferFunc b]
                             []  in
(let new_signals = state_outgoing_signals s in 
(let flag_2 = (case outgoing_signals ((bufferParty b), (bufferFunc b), t1, t2) of
None \<Rightarrow> False |
Some boolean \<Rightarrow>  boolean) in
(s\<lparr>state_flag := flag_1 \<and> flag_2,
   state_ideal_functionalities := new_func_map,
   state_outgoing_signals := new_signals\<rparr>, AdvNone)
))))))))"


fun adv_buffer_action :: "system_state \<Rightarrow> buffer_action \<Rightarrow> protocol_party \<Rightarrow> system_state * adv_input" where
"adv_buffer_action s b party = 
(case bufferAction b of
Peek \<Rightarrow>
(case bufferDirection b of
Incoming \<Rightarrow> adv_peek_incoming_buffer s b party |
Outgoing \<Rightarrow> adv_peek_outgoing_buffer s b party )|
Clock \<Rightarrow> 
(case bufferDirection b of
Incoming \<Rightarrow> adv_clock_incoming_buffer s b party |
Outgoing \<Rightarrow> adv_clock_outgoing_buffer s b party))"


fun adv_send_message :: "system_state \<Rightarrow> send_message \<Rightarrow> protocol_party \<Rightarrow>  system_state * adv_input" where
"adv_send_message s send party =
(let m = sendMessage send in
(let (write_instructions, reply) = party_call party (sendFunc send) m in
(case reply of
None \<Rightarrow> 
(s\<lparr>state_protocol_parties := 
          map_upds (state_protocol_parties s) 
                   [sendParty send] 
                   [do_write_instructions party write_instructions],
state_previous_action := SendMessage send\<rparr>,
       ClockIncomingReply reply) |
Some r \<Rightarrow> 
(s\<lparr>state_previous_action := SendMessage send\<rparr>, ClockIncomingReply reply))))"

fun adv_invoke_environment :: "system_state \<Rightarrow> msg \<Rightarrow>  system_state * adv_input" where
"adv_invoke_environment s m = (s, InvokeEnvironmentReply (env_adv_probe env m))"


fun adv_query_functionality :: 
"system_state \<Rightarrow> query_functionality \<Rightarrow> standard_functionality \<Rightarrow> system_state * adv_input" where
"adv_query_functionality s q fnl = 
(s, QueryFunctionalityReply (fnl_adv_probe fnl (queryMessage q)))"


fun adv_step ::
"system_state  \<times> adv_action \<Rightarrow> system_state \<times> adv_input" where
"adv_step (s, action)  =
(case action of
Empty => no_action s |
CorruptParty p \<Rightarrow> 
  (case state_protocol_parties s p of
  None \<Rightarrow> no_action s |
  Some party \<Rightarrow> adv_corrupt_party s p party) |
BufferAction b \<Rightarrow>
  (case (state_protocol_parties s) (bufferParty b) of 
  None \<Rightarrow> no_action s |
  Some party \<Rightarrow> adv_buffer_action s b party) |
SendMessage send \<Rightarrow>
  (case (state_protocol_parties s) (sendParty send) of
  None \<Rightarrow> no_action s |
  Some party \<Rightarrow> adv_send_message s send party) |
InvokeEnvironment m \<Rightarrow> adv_invoke_environment s m |
QueryFunctionality q \<Rightarrow> 
  (case ideal_functionalities (queryTarget q) of
  None \<Rightarrow>  no_action s |
  Some fnl \<Rightarrow> adv_query_functionality s q fnl))"
end