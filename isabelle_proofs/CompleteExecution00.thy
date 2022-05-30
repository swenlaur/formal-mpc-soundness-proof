theory CompleteExecution00
  imports Main DataTypes
    AdversarialAction ProtocolParty
    StandardFunctionality Environment
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


(* WIP:

Halfway through ClockIncomingBuffer.

Refactoring the code such that buffers are entirely consumed by protocol parties. That is, 
there's no separate Buffer datatype.

Refactored the function to be f : S x A \<rightarrow> S x I.

 *)

(* Breaks bc thinks party is party_id, not 'a protocol_party_scheme.  

(case protocol_parties p of
None \<Rightarrow> (s, AdvNone) |
Some party \<Rightarrow>(case party \<in> state_corrupted_parties s of
True \<Rightarrow> (s, AdvNone) |
False \<Rightarrow>(s\<lparr>state_corrupted_parties := insert party (state_corrupted_parties s),
   state_previous_action := CorruptParty p\<rparr>,
 CorruptionReply (internal_state party))
))

*)
(* Would like to assume that if f is an ideal_functionality, 
then f is always in the domain of other func_id stuffs *)


(* WIP: ClockOutgoing Sucks. *)
(* Okay, so I've done a first pass, but a lot of stuff is still missing! *)
fun adv_step ::
"system_state  \<times> adv_action \<Rightarrow> system_state \<times> adv_input" where
"adv_step (s, action)  = 
(case action of
Empty \<Rightarrow> (s, AdvNone) | 

CorruptParty p \<Rightarrow> (s\<lparr>state_previous_action := CorruptParty p\<rparr>, AdvNone)|

BufferAction b \<Rightarrow>
(case protocol_parties (bufferParty b) of 
None \<Rightarrow> (s, AdvNone)|
Some party \<Rightarrow>
(case bufferAction b of

Peek \<Rightarrow>
(case bufferDirection b of
Incoming \<Rightarrow> 
(case peek_incoming_buffer party (bufferFunc b) (bufferInd b) of
None \<Rightarrow> (s, AdvNone)|
Some m \<Rightarrow> (s\<lparr>state_previous_action := BufferAction b\<rparr>, PeekReply m))|
Outgoing \<Rightarrow> 
(case peek_outgoing_buffer party (bufferFunc b) (bufferInd b) of
None \<Rightarrow> (s, AdvNone)|
Some m \<Rightarrow> (s\<lparr>state_previous_action := BufferAction b\<rparr>, PeekReply m)))|

Clock \<Rightarrow>
(case bufferDirection b of
Incoming \<Rightarrow> 
(let s = (if (\<exists>p.\<exists>func. 
          state_protocol_parties s p = Some party
        \<and> is_corrupted party
        \<and> \<not>(empty_incoming_buffer party func)) 
then s\<lparr>state_flag := False\<rparr> else s) in
(case protocol_parties (bufferParty b) of
None \<Rightarrow> (s, AdvNone) |
Some party \<Rightarrow> 
(let (opt_m, p) = (clock_message party (bufferFunc b) (bufferInd b)) in
(case opt_m of 
None \<Rightarrow> (s, AdvNone) |
Some m \<Rightarrow>
(let (write_instructions, reply) = party_call party (bufferFunc b) m in
(case reply of
None \<Rightarrow> 
(s\<lparr>state_protocol_parties := 
          map_upds (state_protocol_parties s) 
                   [bufferParty b] 
                   [do_write_instructions party write_instructions],
   state_previous_action := BufferAction b\<rparr>,
ClockIncomingReply reply) |
Some r \<Rightarrow> 
(s\<lparr>state_previous_action := BufferAction b\<rparr>, ClockIncomingReply reply)))))))|

Outgoing \<Rightarrow> 
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
(let new_func_map = state_ideal_functionalities s  in
(let new_signals = state_outgoing_signals s in 
(let flag_2 = (case outgoing_signals ((bufferParty b), (bufferFunc b), t1, t2) of
None \<Rightarrow> False |
Some boolean \<Rightarrow>  boolean) in
(s, AdvNone)))))
)))

)))|

SendMessage send \<Rightarrow>
(case protocol_parties (sendParty send) of
None \<Rightarrow> (s, AdvNone) |
Some party \<Rightarrow> 
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
(s\<lparr>state_previous_action := SendMessage send\<rparr>, ClockIncomingReply reply)))))
|

InvokeEnvironment m \<Rightarrow> (s, InvokeEnvironmentReply (env_adv_probe env m)) |

QueryFunctionality q \<Rightarrow> (case ideal_functionalities (queryTarget q) of
None \<Rightarrow>  (s, AdvNone) |
Some fnl \<Rightarrow> (s, QueryFunctionalityReply (fnl_adv_probe fnl (queryMessage q)))))"


(*

(let flag1 = in
(let (opt_m, p) = (clock_message party (bufferFunc b) (bufferInd b)) in
(case opt_m of 
None \<Rightarrow> (s, AdvNone) |
Some m \<Rightarrow>
(let flag2 =
(let (t1, t2) = get_protocol_instances m in
 in
(s\<lparr>state_flag := flag2 \<and> flag1, state_previous_action := BufferAction b\<rparr>, AdvNone)
))))))) |


*)

(* 

(case opt_m of 
None \<Rightarrow> (s, AdvNone) |
Some m \<Rightarrow>
(let (write_instructions, reply) = party_call party f m in
(case reply of
None \<Rightarrow> (s\<lparr>state_protocol_parties := 
          map_upds (state_protocol_parties s) 
                   [bufferParty b] 
                   [do_write_instructions party write_instructions]\<rparr>,
       ClockIncomingReply reply) |
Some r \<Rightarrow> (s, ClockIncomingReply reply))))
)

*)
end
