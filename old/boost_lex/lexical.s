	.file	"lexical.cc"
	.section	.text._ZNSt11char_traitsIcE3eofEv,"axG",@progbits,_ZNSt11char_traitsIcE3eofEv,comdat
	.align 2
	.weak	_ZNSt11char_traitsIcE3eofEv
	.type	_ZNSt11char_traitsIcE3eofEv, @function
_ZNSt11char_traitsIcE3eofEv:
.LFB224:
	pushq	%rbp
.LCFI0:
	movq	%rsp, %rbp
.LCFI1:
	movl	$-1, %eax
	leave
	ret
.LFE224:
	.size	_ZNSt11char_traitsIcE3eofEv, .-_ZNSt11char_traitsIcE3eofEv
.globl __gxx_personality_v0
	.section	.text._ZNSt9exceptionC2Ev,"axG",@progbits,_ZNSt9exceptionC2Ev,comdat
	.align 2
	.weak	_ZNSt9exceptionC2Ev
	.type	_ZNSt9exceptionC2Ev, @function
_ZNSt9exceptionC2Ev:
.LFB241:
	pushq	%rbp
.LCFI2:
	movq	%rsp, %rbp
.LCFI3:
	movq	%rdi, -8(%rbp)
	movl	$_ZTVSt9exception+16, %edx
	movq	-8(%rbp), %rax
	movq	%rdx, (%rax)
	leave
	ret
.LFE241:
	.size	_ZNSt9exceptionC2Ev, .-_ZNSt9exceptionC2Ev
	.section	.text._ZNSt8bad_castC2Ev,"axG",@progbits,_ZNSt8bad_castC2Ev,comdat
	.align 2
	.weak	_ZNSt8bad_castC2Ev
	.type	_ZNSt8bad_castC2Ev, @function
_ZNSt8bad_castC2Ev:
.LFB881:
	pushq	%rbp
.LCFI4:
	movq	%rsp, %rbp
.LCFI5:
	subq	$16, %rsp
.LCFI6:
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rdi
	call	_ZNSt9exceptionC2Ev
	movl	$_ZTVSt8bad_cast+16, %edx
	movq	-8(%rbp), %rax
	movq	%rdx, (%rax)
	leave
	ret
.LFE881:
	.size	_ZNSt8bad_castC2Ev, .-_ZNSt8bad_castC2Ev
	.section	.text._ZStanSt13_Ios_FmtflagsS_,"axG",@progbits,_ZStanSt13_Ios_FmtflagsS_,comdat
	.align 2
	.weak	_ZStanSt13_Ios_FmtflagsS_
	.type	_ZStanSt13_Ios_FmtflagsS_, @function
_ZStanSt13_Ios_FmtflagsS_:
.LFB910:
	pushq	%rbp
.LCFI7:
	movq	%rsp, %rbp
.LCFI8:
	movl	%edi, -4(%rbp)
	movl	%esi, -8(%rbp)
	movl	-4(%rbp), %edx
	movl	-8(%rbp), %eax
	andl	%edx, %eax
	leave
	ret
.LFE910:
	.size	_ZStanSt13_Ios_FmtflagsS_, .-_ZStanSt13_Ios_FmtflagsS_
	.section	.text._ZStaNRSt13_Ios_FmtflagsS_,"axG",@progbits,_ZStaNRSt13_Ios_FmtflagsS_,comdat
	.align 2
	.weak	_ZStaNRSt13_Ios_FmtflagsS_
	.type	_ZStaNRSt13_Ios_FmtflagsS_, @function
_ZStaNRSt13_Ios_FmtflagsS_:
.LFB914:
	pushq	%rbp
.LCFI9:
	movq	%rsp, %rbp
.LCFI10:
	subq	$16, %rsp
.LCFI11:
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movq	-8(%rbp), %rax
	movl	(%rax), %edi
	movl	-12(%rbp), %esi
	call	_ZStanSt13_Ios_FmtflagsS_
	movl	%eax, %edx
	movq	-8(%rbp), %rax
	movl	%edx, (%rax)
	movq	-8(%rbp), %rax
	leave
	ret
.LFE914:
	.size	_ZStaNRSt13_Ios_FmtflagsS_, .-_ZStaNRSt13_Ios_FmtflagsS_
	.section	.text._ZStcoSt13_Ios_Fmtflags,"axG",@progbits,_ZStcoSt13_Ios_Fmtflags,comdat
	.align 2
	.weak	_ZStcoSt13_Ios_Fmtflags
	.type	_ZStcoSt13_Ios_Fmtflags, @function
_ZStcoSt13_Ios_Fmtflags:
.LFB916:
	pushq	%rbp
.LCFI12:
	movq	%rsp, %rbp
.LCFI13:
	movl	%edi, -4(%rbp)
	movl	-4(%rbp), %eax
	notl	%eax
	leave
	ret
.LFE916:
	.size	_ZStcoSt13_Ios_Fmtflags, .-_ZStcoSt13_Ios_Fmtflags
	.section	.text._ZStorSt13_Ios_OpenmodeS_,"axG",@progbits,_ZStorSt13_Ios_OpenmodeS_,comdat
	.align 2
	.weak	_ZStorSt13_Ios_OpenmodeS_
	.type	_ZStorSt13_Ios_OpenmodeS_, @function
_ZStorSt13_Ios_OpenmodeS_:
.LFB918:
	pushq	%rbp
.LCFI14:
	movq	%rsp, %rbp
.LCFI15:
	movl	%edi, -4(%rbp)
	movl	%esi, -8(%rbp)
	movl	-4(%rbp), %edx
	movl	-8(%rbp), %eax
	orl	%edx, %eax
	leave
	ret
.LFE918:
	.size	_ZStorSt13_Ios_OpenmodeS_, .-_ZStorSt13_Ios_OpenmodeS_
	.section	.text._ZNSt8ios_base6unsetfESt13_Ios_Fmtflags,"axG",@progbits,_ZNSt8ios_base6unsetfESt13_Ios_Fmtflags,comdat
	.align 2
	.weak	_ZNSt8ios_base6unsetfESt13_Ios_Fmtflags
	.type	_ZNSt8ios_base6unsetfESt13_Ios_Fmtflags, @function
_ZNSt8ios_base6unsetfESt13_Ios_Fmtflags:
.LFB943:
	pushq	%rbp
.LCFI16:
	movq	%rsp, %rbp
.LCFI17:
	subq	$16, %rsp
.LCFI18:
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movl	-12(%rbp), %edi
	call	_ZStcoSt13_Ios_Fmtflags
	movl	%eax, %esi
	movq	-8(%rbp), %rdi
	addq	$24, %rdi
	call	_ZStaNRSt13_Ios_FmtflagsS_
	leave
	ret
.LFE943:
	.size	_ZNSt8ios_base6unsetfESt13_Ios_Fmtflags, .-_ZNSt8ios_base6unsetfESt13_Ios_Fmtflags
	.section	.text._ZNSt8ios_base9precisionEl,"axG",@progbits,_ZNSt8ios_base9precisionEl,comdat
	.align 2
	.weak	_ZNSt8ios_base9precisionEl
	.type	_ZNSt8ios_base9precisionEl, @function
_ZNSt8ios_base9precisionEl:
.LFB945:
	pushq	%rbp
.LCFI19:
	movq	%rsp, %rbp
.LCFI20:
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	movq	-24(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rax, -8(%rbp)
	movq	-24(%rbp), %rdx
	movq	-32(%rbp), %rax
	movq	%rax, 8(%rdx)
	movq	-8(%rbp), %rax
	leave
	ret
.LFE945:
	.size	_ZNSt8ios_base9precisionEl, .-_ZNSt8ios_base9precisionEl
	.section	.text._ZN5boost16bad_lexical_castC1ERKSt9type_infoS3_,"axG",@progbits,_ZN5boost16bad_lexical_castC1ERKSt9type_infoS3_,comdat
	.align 2
	.weak	_ZN5boost16bad_lexical_castC1ERKSt9type_infoS3_
	.type	_ZN5boost16bad_lexical_castC1ERKSt9type_infoS3_, @function
_ZN5boost16bad_lexical_castC1ERKSt9type_infoS3_:
.LFB1450:
	pushq	%rbp
.LCFI21:
	movq	%rsp, %rbp
.LCFI22:
	subq	$32, %rsp
.LCFI23:
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movq	%rdx, -24(%rbp)
	movq	-8(%rbp), %rdi
	call	_ZNSt8bad_castC2Ev
	movl	$_ZTVN5boost16bad_lexical_castE+16, %edx
	movq	-8(%rbp), %rax
	movq	%rdx, (%rax)
	movq	-8(%rbp), %rdx
	movq	-16(%rbp), %rax
	movq	%rax, 8(%rdx)
	movq	-8(%rbp), %rdx
	movq	-24(%rbp), %rax
	movq	%rax, 16(%rdx)
	leave
	ret
.LFE1450:
	.size	_ZN5boost16bad_lexical_castC1ERKSt9type_infoS3_, .-_ZN5boost16bad_lexical_castC1ERKSt9type_infoS3_
	.section	.rodata
	.align 8
.LC0:
	.string	"bad lexical cast: source type value could not be interpreted as target"
	.section	.text._ZNK5boost16bad_lexical_cast4whatEv,"axG",@progbits,_ZNK5boost16bad_lexical_cast4whatEv,comdat
	.align 2
	.weak	_ZNK5boost16bad_lexical_cast4whatEv
	.type	_ZNK5boost16bad_lexical_cast4whatEv, @function
_ZNK5boost16bad_lexical_cast4whatEv:
.LFB1453:
	pushq	%rbp
.LCFI24:
	movq	%rsp, %rbp
.LCFI25:
	movq	%rdi, -8(%rbp)
	movl	$.LC0, %eax
	leave
	ret
.LFE1453:
	.size	_ZNK5boost16bad_lexical_cast4whatEv, .-_ZNK5boost16bad_lexical_cast4whatEv
	.section	.text._ZNSt9exceptionC2ERKS_,"axG",@progbits,_ZNSt9exceptionC2ERKS_,comdat
	.align 2
	.weak	_ZNSt9exceptionC2ERKS_
	.type	_ZNSt9exceptionC2ERKS_, @function
_ZNSt9exceptionC2ERKS_:
.LFB1469:
	pushq	%rbp
.LCFI26:
	movq	%rsp, %rbp
.LCFI27:
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movl	$_ZTVSt9exception+16, %edx
	movq	-8(%rbp), %rax
	movq	%rdx, (%rax)
	leave
	ret
.LFE1469:
	.size	_ZNSt9exceptionC2ERKS_, .-_ZNSt9exceptionC2ERKS_
	.section	.text._ZNSt8bad_castC2ERKS_,"axG",@progbits,_ZNSt8bad_castC2ERKS_,comdat
	.align 2
	.weak	_ZNSt8bad_castC2ERKS_
	.type	_ZNSt8bad_castC2ERKS_, @function
_ZNSt8bad_castC2ERKS_:
.LFB1471:
	pushq	%rbp
.LCFI28:
	movq	%rsp, %rbp
.LCFI29:
	subq	$16, %rsp
.LCFI30:
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movq	-16(%rbp), %rsi
	movq	-8(%rbp), %rdi
	call	_ZNSt9exceptionC2ERKS_
	movl	$_ZTVSt8bad_cast+16, %edx
	movq	-8(%rbp), %rax
	movq	%rdx, (%rax)
	leave
	ret
.LFE1471:
	.size	_ZNSt8bad_castC2ERKS_, .-_ZNSt8bad_castC2ERKS_
	.section	.text._ZN5boost16bad_lexical_castC1ERKS0_,"axG",@progbits,_ZN5boost16bad_lexical_castC1ERKS0_,comdat
	.align 2
	.weak	_ZN5boost16bad_lexical_castC1ERKS0_
	.type	_ZN5boost16bad_lexical_castC1ERKS0_, @function
_ZN5boost16bad_lexical_castC1ERKS0_:
.LFB1474:
	pushq	%rbp
.LCFI31:
	movq	%rsp, %rbp
.LCFI32:
	subq	$16, %rsp
.LCFI33:
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movq	-16(%rbp), %rsi
	movq	-8(%rbp), %rdi
	call	_ZNSt8bad_castC2ERKS_
	movl	$_ZTVN5boost16bad_lexical_castE+16, %edx
	movq	-8(%rbp), %rax
	movq	%rdx, (%rax)
	movq	-16(%rbp), %rax
	movq	8(%rax), %rdx
	movq	-8(%rbp), %rax
	movq	%rdx, 8(%rax)
	movq	-16(%rbp), %rax
	movq	16(%rax), %rdx
	movq	-8(%rbp), %rax
	movq	%rdx, 16(%rax)
	leave
	ret
.LFE1474:
	.size	_ZN5boost16bad_lexical_castC1ERKS0_, .-_ZN5boost16bad_lexical_castC1ERKS0_
	.section	.text._ZN5boost6detail14lexical_streamIdSsEC1Ev,"axG",@progbits,_ZN5boost6detail14lexical_streamIdSsEC1Ev,comdat
	.align 2
	.weak	_ZN5boost6detail14lexical_streamIdSsEC1Ev
	.type	_ZN5boost6detail14lexical_streamIdSsEC1Ev, @function
_ZN5boost6detail14lexical_streamIdSsEC1Ev:
.LFB1510:
	pushq	%rbp
.LCFI34:
	movq	%rsp, %rbp
.LCFI35:
	subq	$16, %rsp
.LCFI36:
	movq	%rdi, -8(%rbp)
	movl	$8, %esi
	movl	$16, %edi
	call	_ZStorSt13_Ios_OpenmodeS_
	movl	%eax, %esi
	movq	-8(%rbp), %rdi
	call	_ZNSt18basic_stringstreamIcSt11char_traitsIcESaIcEEC1ESt13_Ios_Openmode
	movq	-8(%rbp), %rdi
	addq	$104, %rdi
	movl	$4096, %esi
	call	_ZNSt8ios_base6unsetfESt13_Ios_Fmtflags
	movq	-8(%rbp), %rdi
	addq	$104, %rdi
	movl	$16, %esi
	call	_ZNSt8ios_base9precisionEl
	leave
	ret
.LFE1510:
	.size	_ZN5boost6detail14lexical_streamIdSsEC1Ev, .-_ZN5boost6detail14lexical_streamIdSsEC1Ev
	.section	.text._ZN5boost6detail14lexical_streamIdSsED1Ev,"axG",@progbits,_ZN5boost6detail14lexical_streamIdSsED1Ev,comdat
	.align 2
	.weak	_ZN5boost6detail14lexical_streamIdSsED1Ev
	.type	_ZN5boost6detail14lexical_streamIdSsED1Ev, @function
_ZN5boost6detail14lexical_streamIdSsED1Ev:
.LFB1513:
	pushq	%rbp
.LCFI37:
	movq	%rsp, %rbp
.LCFI38:
	subq	$16, %rsp
.LCFI39:
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rdi
	call	_ZNSt18basic_stringstreamIcSt11char_traitsIcESaIcEED1Ev
	leave
	ret
.LFE1513:
	.size	_ZN5boost6detail14lexical_streamIdSsED1Ev, .-_ZN5boost6detail14lexical_streamIdSsED1Ev
	.section	.text._ZN5boost6detail14lexical_streamIdSsElsERKSs,"axG",@progbits,_ZN5boost6detail14lexical_streamIdSsElsERKSs,comdat
	.align 2
	.weak	_ZN5boost6detail14lexical_streamIdSsElsERKSs
	.type	_ZN5boost6detail14lexical_streamIdSsElsERKSs, @function
_ZN5boost6detail14lexical_streamIdSsElsERKSs:
.LFB1515:
	pushq	%rbp
.LCFI40:
	movq	%rsp, %rbp
.LCFI41:
	subq	$16, %rsp
.LCFI42:
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movq	-8(%rbp), %rdi
	addq	$16, %rdi
	movq	-16(%rbp), %rsi
	call	_ZStlsIcSt11char_traitsIcESaIcEERSt13basic_ostreamIT_T0_ES7_RKSbIS4_S5_T1_E
	movq	%rax, %rdx
	movq	(%rax), %rax
	subq	$24, %rax
	movq	(%rax), %rax
	leaq	(%rdx,%rax), %rdi
	call	_ZNKSt9basic_iosIcSt11char_traitsIcEE4failEv
	xorl	$1, %eax
	movzbl	%al, %eax
	leave
	ret
.LFE1515:
	.size	_ZN5boost6detail14lexical_streamIdSsElsERKSs, .-_ZN5boost6detail14lexical_streamIdSsElsERKSs
	.section	.text._ZN5boost6detail14lexical_streamIdSsErsIdEEbRT_,"axG",@progbits,_ZN5boost6detail14lexical_streamIdSsErsIdEEbRT_,comdat
	.align 2
	.weak	_ZN5boost6detail14lexical_streamIdSsErsIdEEbRT_
	.type	_ZN5boost6detail14lexical_streamIdSsErsIdEEbRT_, @function
_ZN5boost6detail14lexical_streamIdSsErsIdEEbRT_:
.LFB1514:
	pushq	%rbp
.LCFI43:
	movq	%rsp, %rbp
.LCFI44:
	pushq	%rbx
.LCFI45:
	subq	$24, %rsp
.LCFI46:
	movq	%rdi, -16(%rbp)
	movq	%rsi, -24(%rbp)
	movq	-16(%rbp), %rdi
	movq	-24(%rbp), %rsi
	call	_ZNSirsERd
	movq	%rax, %rdx
	movq	(%rax), %rax
	subq	$24, %rax
	movq	(%rax), %rax
	leaq	(%rdx,%rax), %rdi
	call	_ZNKSt9basic_iosIcSt11char_traitsIcEEcvPvEv
	testq	%rax, %rax
	je	.L37
	movq	-16(%rbp), %rdi
	call	_ZNSi3getEv
	movl	%eax, %ebx
	call	_ZNSt11char_traitsIcE3eofEv
	cmpl	%eax, %ebx
	jne	.L37
	movb	$1, -25(%rbp)
	jmp	.L40
.L37:
	movb	$0, -25(%rbp)
.L40:
	movzbl	-25(%rbp), %eax
	addq	$24, %rsp
	popq	%rbx
	leave
	ret
.LFE1514:
	.size	_ZN5boost6detail14lexical_streamIdSsErsIdEEbRT_, .-_ZN5boost6detail14lexical_streamIdSsErsIdEEbRT_
	.section	.text._ZN5boost16bad_lexical_castD0Ev,"axG",@progbits,_ZN5boost16bad_lexical_castD0Ev,comdat
	.align 2
	.weak	_ZN5boost16bad_lexical_castD0Ev
	.type	_ZN5boost16bad_lexical_castD0Ev, @function
_ZN5boost16bad_lexical_castD0Ev:
.LFB1457:
	pushq	%rbp
.LCFI47:
	movq	%rsp, %rbp
.LCFI48:
	subq	$16, %rsp
.LCFI49:
	movq	%rdi, -8(%rbp)
	movl	$_ZTVN5boost16bad_lexical_castE+16, %edx
	movq	-8(%rbp), %rax
	movq	%rdx, (%rax)
	movq	-8(%rbp), %rdi
	call	_ZNSt8bad_castD2Ev
	movl	$1, %eax
	testb	%al, %al
	je	.L46
	movq	-8(%rbp), %rdi
	call	_ZdlPv
.L46:
	leave
	ret
.LFE1457:
	.size	_ZN5boost16bad_lexical_castD0Ev, .-_ZN5boost16bad_lexical_castD0Ev
	.section	.text._ZN5boost16bad_lexical_castD1Ev,"axG",@progbits,_ZN5boost16bad_lexical_castD1Ev,comdat
	.align 2
	.weak	_ZN5boost16bad_lexical_castD1Ev
	.type	_ZN5boost16bad_lexical_castD1Ev, @function
_ZN5boost16bad_lexical_castD1Ev:
.LFB1456:
	pushq	%rbp
.LCFI50:
	movq	%rsp, %rbp
.LCFI51:
	subq	$16, %rsp
.LCFI52:
	movq	%rdi, -8(%rbp)
	movl	$_ZTVN5boost16bad_lexical_castE+16, %edx
	movq	-8(%rbp), %rax
	movq	%rdx, (%rax)
	movq	-8(%rbp), %rdi
	call	_ZNSt8bad_castD2Ev
	movl	$0, %eax
	testb	%al, %al
	je	.L51
	movq	-8(%rbp), %rdi
	call	_ZdlPv
.L51:
	leave
	ret
.LFE1456:
	.size	_ZN5boost16bad_lexical_castD1Ev, .-_ZN5boost16bad_lexical_castD1Ev
	.section	.text._ZN5boost15throw_exceptionINS_16bad_lexical_castEEEvRKT_,"axG",@progbits,_ZN5boost15throw_exceptionINS_16bad_lexical_castEEEvRKT_,comdat
	.align 2
	.weak	_ZN5boost15throw_exceptionINS_16bad_lexical_castEEEvRKT_
	.type	_ZN5boost15throw_exceptionINS_16bad_lexical_castEEEvRKT_, @function
_ZN5boost15throw_exceptionINS_16bad_lexical_castEEEvRKT_:
.LFB1516:
	pushq	%rbp
.LCFI53:
	movq	%rsp, %rbp
.LCFI54:
	pushq	%rbx
.LCFI55:
	subq	$8, %rsp
.LCFI56:
	movq	%rdi, -16(%rbp)
	movl	$24, %edi
	call	__cxa_allocate_exception
	movq	%rax, %rbx
	movq	%rbx, %rdi
	movq	-16(%rbp), %rsi
	call	_ZN5boost16bad_lexical_castC1ERKS0_
	movl	$_ZN5boost16bad_lexical_castD1Ev, %edx
	movl	$_ZTIN5boost16bad_lexical_castE, %esi
	movq	%rbx, %rdi
	call	__cxa_throw
.LFE1516:
	.size	_ZN5boost15throw_exceptionINS_16bad_lexical_castEEEvRKT_, .-_ZN5boost15throw_exceptionINS_16bad_lexical_castEEEvRKT_
.globl _Unwind_Resume
	.section	.text._ZN5boost12lexical_castIdSsEET_RKT0_,"axG",@progbits,_ZN5boost12lexical_castIdSsEET_RKT0_,comdat
	.align 2
	.weak	_ZN5boost12lexical_castIdSsEET_RKT0_
	.type	_ZN5boost12lexical_castIdSsEET_RKT0_, @function
_ZN5boost12lexical_castIdSsEET_RKT0_:
.LFB1494:
	pushq	%rbp
.LCFI57:
	movq	%rsp, %rbp
.LCFI58:
	pushq	%rbx
.LCFI59:
	subq	$456, %rsp
.LCFI60:
	movq	%rdi, -440(%rbp)
	leaq	-432(%rbp), %rdi
.LEHB0:
	call	_ZN5boost6detail14lexical_streamIdSsEC1Ev
.LEHE0:
	movq	-440(%rbp), %rsi
	leaq	-432(%rbp), %rdi
.LEHB1:
	call	_ZN5boost6detail14lexical_streamIdSsElsERKSs
	xorl	$1, %eax
	testb	%al, %al
	jne	.L55
	leaq	-56(%rbp), %rsi
	leaq	-432(%rbp), %rdi
	call	_ZN5boost6detail14lexical_streamIdSsErsIdEEbRT_
.LEHE1:
	xorl	$1, %eax
	testb	%al, %al
	je	.L57
.L55:
	movb	$1, -441(%rbp)
	jmp	.L58
.L57:
	movb	$0, -441(%rbp)
.L58:
	movzbl	-441(%rbp), %eax
	testb	%al, %al
	je	.L59
	movl	$_ZTId, %edx
	movl	$_ZTISs, %esi
	leaq	-48(%rbp), %rdi
	call	_ZN5boost16bad_lexical_castC1ERKSt9type_infoS3_
	leaq	-48(%rbp), %rdi
.LEHB2:
	call	_ZN5boost15throw_exceptionINS_16bad_lexical_castEEEvRKT_
.LEHE2:
	leaq	-48(%rbp), %rdi
	call	_ZN5boost16bad_lexical_castD1Ev
	jmp	.L59
.L64:
	movq	%rax, -464(%rbp)
.L61:
	movq	-464(%rbp), %rbx
	leaq	-48(%rbp), %rdi
	call	_ZN5boost16bad_lexical_castD1Ev
	movq	%rbx, -464(%rbp)
	jmp	.L62
.L59:
	movq	-56(%rbp), %rbx
	leaq	-432(%rbp), %rdi
.LEHB3:
	call	_ZN5boost6detail14lexical_streamIdSsED1Ev
.LEHE3:
	movq	%rbx, -456(%rbp)
	jmp	.L54
.L65:
	movq	%rax, -464(%rbp)
.L62:
	movq	-464(%rbp), %rbx
	leaq	-432(%rbp), %rdi
	call	_ZN5boost6detail14lexical_streamIdSsED1Ev
	movq	%rbx, -464(%rbp)
	movq	-464(%rbp), %rdi
.LEHB4:
	call	_Unwind_Resume
.LEHE4:
.L54:
	movsd	-456(%rbp), %xmm0
	addq	$456, %rsp
	popq	%rbx
	leave
	ret
.LFE1494:
	.size	_ZN5boost12lexical_castIdSsEET_RKT0_, .-_ZN5boost12lexical_castIdSsEET_RKT0_
	.section	.gcc_except_table,"a",@progbits
.LLSDA1494:
	.byte	0xff
	.byte	0xff
	.byte	0x1
	.uleb128 .LLSDACSE1494-.LLSDACSB1494
.LLSDACSB1494:
	.uleb128 .LEHB0-.LFB1494
	.uleb128 .LEHE0-.LEHB0
	.uleb128 0x0
	.uleb128 0x0
	.uleb128 .LEHB1-.LFB1494
	.uleb128 .LEHE1-.LEHB1
	.uleb128 .L65-.LFB1494
	.uleb128 0x0
	.uleb128 .LEHB2-.LFB1494
	.uleb128 .LEHE2-.LEHB2
	.uleb128 .L64-.LFB1494
	.uleb128 0x0
	.uleb128 .LEHB3-.LFB1494
	.uleb128 .LEHE3-.LEHB3
	.uleb128 0x0
	.uleb128 0x0
	.uleb128 .LEHB4-.LFB1494
	.uleb128 .LEHE4-.LEHB4
	.uleb128 0x0
	.uleb128 0x0
.LLSDACSE1494:
	.section	.text._ZN5boost12lexical_castIdSsEET_RKT0_,"axG",@progbits,_ZN5boost12lexical_castIdSsEET_RKT0_,comdat
	.section	.rodata
.LC1:
	.string	"666.6"
.LC2:
	.string	"%lf\n"
.LC3:
	.string	"***SHABAMA***"
	.text
	.align 2
.globl main
	.type	main, @function
main:
.LFB1465:
	pushq	%rbp
.LCFI61:
	movq	%rsp, %rbp
.LCFI62:
	pushq	%rbx
.LCFI63:
	subq	$88, %rsp
.LCFI64:
	leaq	-17(%rbp), %rdi
	call	_ZNSaIcEC1Ev
	leaq	-17(%rbp), %rdx
	leaq	-32(%rbp), %rdi
	movl	$.LC1, %esi
.LEHB5:
	call	_ZNSsC1EPKcRKSaIcE
.LEHE5:
	leaq	-17(%rbp), %rdi
	call	_ZNSaIcED1Ev
	leaq	-32(%rbp), %rdi
.LEHB6:
	call	_ZN5boost12lexical_castIdSsEET_RKT0_
.LEHE6:
	movsd	%xmm0, -72(%rbp)
	jmp	.L67
.L81:
	movq	%rax, -88(%rbp)
.L68:
	movq	-88(%rbp), %rbx
	leaq	-17(%rbp), %rdi
	call	_ZNSaIcED1Ev
	movq	%rbx, -88(%rbp)
	movq	-88(%rbp), %rdi
.LEHB7:
	call	_Unwind_Resume
.LEHE7:
.L67:
	movsd	-72(%rbp), %xmm0
	movl	$.LC2, %edi
	movl	$1, %eax
.LEHB8:
	call	printf
.LEHE8:
	jmp	.L69
.L79:
	movq	%rax, -88(%rbp)
	cmpq	$1, %rdx
	je	.L70
	jmp	.L74
.L70:
	movq	-88(%rbp), %rdi
	call	__cxa_get_exception_ptr
	movq	%rax, %rsi
	leaq	-64(%rbp), %rdi
	call	_ZN5boost16bad_lexical_castC1ERKS0_
	movq	-88(%rbp), %rdi
	call	__cxa_begin_catch
	movl	$.LC3, %edi
.LEHB9:
	call	puts
.LEHE9:
	leaq	-64(%rbp), %rdi
	call	_ZN5boost16bad_lexical_castD1Ev
	call	__cxa_end_catch
	jmp	.L69
.L77:
	movq	%rax, -88(%rbp)
.L72:
	movq	-88(%rbp), %rbx
	leaq	-64(%rbp), %rdi
	call	_ZN5boost16bad_lexical_castD1Ev
	movq	%rbx, -88(%rbp)
.L78:
.L73:
	movq	-88(%rbp), %rbx
	call	__cxa_end_catch
	movq	%rbx, -88(%rbp)
	jmp	.L74
.L69:
	movl	$0, %ebx
	leaq	-32(%rbp), %rdi
.LEHB10:
	call	_ZNSsD1Ev
.LEHE10:
	movl	%ebx, -76(%rbp)
	jmp	.L66
.L80:
.L74:
	movq	-88(%rbp), %rbx
	leaq	-32(%rbp), %rdi
	call	_ZNSsD1Ev
	movq	%rbx, -88(%rbp)
	movq	-88(%rbp), %rdi
.LEHB11:
	call	_Unwind_Resume
.LEHE11:
.L66:
	movl	-76(%rbp), %eax
	addq	$88, %rsp
	popq	%rbx
	leave
	ret
.LFE1465:
	.size	main, .-main
	.section	.gcc_except_table
	.align 4
.LLSDA1465:
	.byte	0xff
	.byte	0x3
	.uleb128 .LLSDATT1465-.LLSDATTD1465
.LLSDATTD1465:
	.byte	0x1
	.uleb128 .LLSDACSE1465-.LLSDACSB1465
.LLSDACSB1465:
	.uleb128 .LEHB5-.LFB1465
	.uleb128 .LEHE5-.LEHB5
	.uleb128 .L81-.LFB1465
	.uleb128 0x0
	.uleb128 .LEHB6-.LFB1465
	.uleb128 .LEHE6-.LEHB6
	.uleb128 .L79-.LFB1465
	.uleb128 0x3
	.uleb128 .LEHB7-.LFB1465
	.uleb128 .LEHE7-.LEHB7
	.uleb128 0x0
	.uleb128 0x0
	.uleb128 .LEHB8-.LFB1465
	.uleb128 .LEHE8-.LEHB8
	.uleb128 .L79-.LFB1465
	.uleb128 0x3
	.uleb128 .LEHB9-.LFB1465
	.uleb128 .LEHE9-.LEHB9
	.uleb128 .L77-.LFB1465
	.uleb128 0x0
	.uleb128 .LEHB10-.LFB1465
	.uleb128 .LEHE10-.LEHB10
	.uleb128 0x0
	.uleb128 0x0
	.uleb128 .LEHB11-.LFB1465
	.uleb128 .LEHE11-.LEHB11
	.uleb128 0x0
	.uleb128 0x0
.LLSDACSE1465:
	.byte	0x0
	.byte	0x0
	.byte	0x1
	.byte	0x7d
	.align 4
	.long	_ZTIN5boost16bad_lexical_castE
.LLSDATT1465:
	.text
	.weak	_ZTISs
	.section	.rodata._ZTISs,"aG",@progbits,_ZTISs,comdat
	.align 16
	.type	_ZTISs, @object
	.size	_ZTISs, 16
_ZTISs:
	.quad	_ZTVN10__cxxabiv117__class_type_infoE+16
	.quad	_ZTSSs
	.weak	_ZTSSs
	.section	.rodata._ZTSSs,"aG",@progbits,_ZTSSs,comdat
	.type	_ZTSSs, @object
	.size	_ZTSSs, 3
_ZTSSs:
	.string	"Ss"
	.weak	_ZTVN5boost16bad_lexical_castE
	.section	.rodata._ZTVN5boost16bad_lexical_castE,"aG",@progbits,_ZTVN5boost16bad_lexical_castE,comdat
	.align 32
	.type	_ZTVN5boost16bad_lexical_castE, @object
	.size	_ZTVN5boost16bad_lexical_castE, 40
_ZTVN5boost16bad_lexical_castE:
	.quad	0
	.quad	_ZTIN5boost16bad_lexical_castE
	.quad	_ZN5boost16bad_lexical_castD1Ev
	.quad	_ZN5boost16bad_lexical_castD0Ev
	.quad	_ZNK5boost16bad_lexical_cast4whatEv
	.weak	_ZTIN5boost16bad_lexical_castE
	.section	.rodata._ZTIN5boost16bad_lexical_castE,"aG",@progbits,_ZTIN5boost16bad_lexical_castE,comdat
	.align 16
	.type	_ZTIN5boost16bad_lexical_castE, @object
	.size	_ZTIN5boost16bad_lexical_castE, 24
_ZTIN5boost16bad_lexical_castE:
	.quad	_ZTVN10__cxxabiv120__si_class_type_infoE+16
	.quad	_ZTSN5boost16bad_lexical_castE
	.quad	_ZTISt8bad_cast
	.weak	_ZTSN5boost16bad_lexical_castE
	.section	.rodata._ZTSN5boost16bad_lexical_castE,"aG",@progbits,_ZTSN5boost16bad_lexical_castE,comdat
	.align 16
	.type	_ZTSN5boost16bad_lexical_castE, @object
	.size	_ZTSN5boost16bad_lexical_castE, 27
_ZTSN5boost16bad_lexical_castE:
	.string	"N5boost16bad_lexical_castE"
	.weakref	_Z20__gthrw_pthread_oncePiPFvvE,pthread_once
	.weakref	_Z27__gthrw_pthread_getspecificj,pthread_getspecific
	.weakref	_Z27__gthrw_pthread_setspecificjPKv,pthread_setspecific
	.weakref	_Z22__gthrw_pthread_createPmPK14pthread_attr_tPFPvS3_ES3_,pthread_create
	.weakref	_Z22__gthrw_pthread_cancelm,pthread_cancel
	.weakref	_Z26__gthrw_pthread_mutex_lockP15pthread_mutex_t,pthread_mutex_lock
	.weakref	_Z29__gthrw_pthread_mutex_trylockP15pthread_mutex_t,pthread_mutex_trylock
	.weakref	_Z28__gthrw_pthread_mutex_unlockP15pthread_mutex_t,pthread_mutex_unlock
	.weakref	_Z26__gthrw_pthread_mutex_initP15pthread_mutex_tPK19pthread_mutexattr_t,pthread_mutex_init
	.weakref	_Z30__gthrw_pthread_cond_broadcastP14pthread_cond_t,pthread_cond_broadcast
	.weakref	_Z25__gthrw_pthread_cond_waitP14pthread_cond_tP15pthread_mutex_t,pthread_cond_wait
	.weakref	_Z26__gthrw_pthread_key_createPjPFvPvE,pthread_key_create
	.weakref	_Z26__gthrw_pthread_key_deletej,pthread_key_delete
	.weakref	_Z30__gthrw_pthread_mutexattr_initP19pthread_mutexattr_t,pthread_mutexattr_init
	.weakref	_Z33__gthrw_pthread_mutexattr_settypeP19pthread_mutexattr_ti,pthread_mutexattr_settype
	.weakref	_Z33__gthrw_pthread_mutexattr_destroyP19pthread_mutexattr_t,pthread_mutexattr_destroy
	.section	.eh_frame,"a",@progbits
.Lframe1:
	.long	.LECIE1-.LSCIE1
.LSCIE1:
	.long	0x0
	.byte	0x1
	.string	"zPLR"
	.uleb128 0x1
	.sleb128 -8
	.byte	0x10
	.uleb128 0x7
	.byte	0x3
	.long	__gxx_personality_v0
	.byte	0x3
	.byte	0x3
	.byte	0xc
	.uleb128 0x7
	.uleb128 0x8
	.byte	0x90
	.uleb128 0x1
	.align 8
.LECIE1:
.LSFDE1:
	.long	.LEFDE1-.LASFDE1
.LASFDE1:
	.long	.LASFDE1-.Lframe1
	.long	.LFB224
	.long	.LFE224-.LFB224
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI0-.LFB224
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI1-.LCFI0
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE1:
.LSFDE3:
	.long	.LEFDE3-.LASFDE3
.LASFDE3:
	.long	.LASFDE3-.Lframe1
	.long	.LFB241
	.long	.LFE241-.LFB241
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI2-.LFB241
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI3-.LCFI2
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE3:
.LSFDE5:
	.long	.LEFDE5-.LASFDE5
.LASFDE5:
	.long	.LASFDE5-.Lframe1
	.long	.LFB881
	.long	.LFE881-.LFB881
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI4-.LFB881
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI5-.LCFI4
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE5:
.LSFDE7:
	.long	.LEFDE7-.LASFDE7
.LASFDE7:
	.long	.LASFDE7-.Lframe1
	.long	.LFB910
	.long	.LFE910-.LFB910
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI7-.LFB910
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI8-.LCFI7
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE7:
.LSFDE9:
	.long	.LEFDE9-.LASFDE9
.LASFDE9:
	.long	.LASFDE9-.Lframe1
	.long	.LFB914
	.long	.LFE914-.LFB914
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI9-.LFB914
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI10-.LCFI9
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE9:
.LSFDE11:
	.long	.LEFDE11-.LASFDE11
.LASFDE11:
	.long	.LASFDE11-.Lframe1
	.long	.LFB916
	.long	.LFE916-.LFB916
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI12-.LFB916
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI13-.LCFI12
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE11:
.LSFDE13:
	.long	.LEFDE13-.LASFDE13
.LASFDE13:
	.long	.LASFDE13-.Lframe1
	.long	.LFB918
	.long	.LFE918-.LFB918
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI14-.LFB918
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI15-.LCFI14
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE13:
.LSFDE15:
	.long	.LEFDE15-.LASFDE15
.LASFDE15:
	.long	.LASFDE15-.Lframe1
	.long	.LFB943
	.long	.LFE943-.LFB943
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI16-.LFB943
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI17-.LCFI16
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE15:
.LSFDE17:
	.long	.LEFDE17-.LASFDE17
.LASFDE17:
	.long	.LASFDE17-.Lframe1
	.long	.LFB945
	.long	.LFE945-.LFB945
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI19-.LFB945
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI20-.LCFI19
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE17:
.LSFDE19:
	.long	.LEFDE19-.LASFDE19
.LASFDE19:
	.long	.LASFDE19-.Lframe1
	.long	.LFB1450
	.long	.LFE1450-.LFB1450
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI21-.LFB1450
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI22-.LCFI21
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE19:
.LSFDE21:
	.long	.LEFDE21-.LASFDE21
.LASFDE21:
	.long	.LASFDE21-.Lframe1
	.long	.LFB1453
	.long	.LFE1453-.LFB1453
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI24-.LFB1453
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI25-.LCFI24
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE21:
.LSFDE23:
	.long	.LEFDE23-.LASFDE23
.LASFDE23:
	.long	.LASFDE23-.Lframe1
	.long	.LFB1469
	.long	.LFE1469-.LFB1469
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI26-.LFB1469
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI27-.LCFI26
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE23:
.LSFDE25:
	.long	.LEFDE25-.LASFDE25
.LASFDE25:
	.long	.LASFDE25-.Lframe1
	.long	.LFB1471
	.long	.LFE1471-.LFB1471
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI28-.LFB1471
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI29-.LCFI28
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE25:
.LSFDE27:
	.long	.LEFDE27-.LASFDE27
.LASFDE27:
	.long	.LASFDE27-.Lframe1
	.long	.LFB1474
	.long	.LFE1474-.LFB1474
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI31-.LFB1474
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI32-.LCFI31
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE27:
.LSFDE29:
	.long	.LEFDE29-.LASFDE29
.LASFDE29:
	.long	.LASFDE29-.Lframe1
	.long	.LFB1510
	.long	.LFE1510-.LFB1510
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI34-.LFB1510
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI35-.LCFI34
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE29:
.LSFDE31:
	.long	.LEFDE31-.LASFDE31
.LASFDE31:
	.long	.LASFDE31-.Lframe1
	.long	.LFB1513
	.long	.LFE1513-.LFB1513
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI37-.LFB1513
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI38-.LCFI37
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE31:
.LSFDE33:
	.long	.LEFDE33-.LASFDE33
.LASFDE33:
	.long	.LASFDE33-.Lframe1
	.long	.LFB1515
	.long	.LFE1515-.LFB1515
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI40-.LFB1515
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI41-.LCFI40
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE33:
.LSFDE35:
	.long	.LEFDE35-.LASFDE35
.LASFDE35:
	.long	.LASFDE35-.Lframe1
	.long	.LFB1514
	.long	.LFE1514-.LFB1514
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI43-.LFB1514
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI44-.LCFI43
	.byte	0xd
	.uleb128 0x6
	.byte	0x4
	.long	.LCFI46-.LCFI44
	.byte	0x83
	.uleb128 0x3
	.align 8
.LEFDE35:
.LSFDE37:
	.long	.LEFDE37-.LASFDE37
.LASFDE37:
	.long	.LASFDE37-.Lframe1
	.long	.LFB1457
	.long	.LFE1457-.LFB1457
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI47-.LFB1457
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI48-.LCFI47
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE37:
.LSFDE39:
	.long	.LEFDE39-.LASFDE39
.LASFDE39:
	.long	.LASFDE39-.Lframe1
	.long	.LFB1456
	.long	.LFE1456-.LFB1456
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI50-.LFB1456
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI51-.LCFI50
	.byte	0xd
	.uleb128 0x6
	.align 8
.LEFDE39:
.LSFDE41:
	.long	.LEFDE41-.LASFDE41
.LASFDE41:
	.long	.LASFDE41-.Lframe1
	.long	.LFB1516
	.long	.LFE1516-.LFB1516
	.uleb128 0x4
	.long	0x0
	.byte	0x4
	.long	.LCFI53-.LFB1516
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI54-.LCFI53
	.byte	0xd
	.uleb128 0x6
	.byte	0x4
	.long	.LCFI56-.LCFI54
	.byte	0x83
	.uleb128 0x3
	.align 8
.LEFDE41:
.LSFDE43:
	.long	.LEFDE43-.LASFDE43
.LASFDE43:
	.long	.LASFDE43-.Lframe1
	.long	.LFB1494
	.long	.LFE1494-.LFB1494
	.uleb128 0x4
	.long	.LLSDA1494
	.byte	0x4
	.long	.LCFI57-.LFB1494
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI58-.LCFI57
	.byte	0xd
	.uleb128 0x6
	.byte	0x4
	.long	.LCFI60-.LCFI58
	.byte	0x83
	.uleb128 0x3
	.align 8
.LEFDE43:
.LSFDE45:
	.long	.LEFDE45-.LASFDE45
.LASFDE45:
	.long	.LASFDE45-.Lframe1
	.long	.LFB1465
	.long	.LFE1465-.LFB1465
	.uleb128 0x4
	.long	.LLSDA1465
	.byte	0x4
	.long	.LCFI61-.LFB1465
	.byte	0xe
	.uleb128 0x10
	.byte	0x86
	.uleb128 0x2
	.byte	0x4
	.long	.LCFI62-.LCFI61
	.byte	0xd
	.uleb128 0x6
	.byte	0x4
	.long	.LCFI64-.LCFI62
	.byte	0x83
	.uleb128 0x3
	.align 8
.LEFDE45:
	.ident	"GCC: (GNU) 4.1.2 20080704 (Red Hat 4.1.2-52)"
	.section	.note.GNU-stack,"",@progbits
