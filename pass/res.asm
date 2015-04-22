
pass:     file format elf64-x86-64


Disassembly of section .init:

0000000000400560 <_init>:
  400560:	48 83 ec 08          	sub    $0x8,%rsp
  400564:	48 8b 05 8d 0a 20 00 	mov    0x200a8d(%rip),%rax        # 600ff8 <_DYNAMIC+0x1d0>
  40056b:	48 85 c0             	test   %rax,%rax
  40056e:	74 05                	je     400575 <_init+0x15>
  400570:	e8 8b 00 00 00       	callq  400600 <__gmon_start__@plt>
  400575:	48 83 c4 08          	add    $0x8,%rsp
  400579:	c3                   	retq   

Disassembly of section .plt:

0000000000400580 <strncmp@plt-0x10>:
  400580:	ff 35 82 0a 20 00    	pushq  0x200a82(%rip)        # 601008 <_GLOBAL_OFFSET_TABLE_+0x8>
  400586:	ff 25 84 0a 20 00    	jmpq   *0x200a84(%rip)        # 601010 <_GLOBAL_OFFSET_TABLE_+0x10>
  40058c:	0f 1f 40 00          	nopl   0x0(%rax)

0000000000400590 <strncmp@plt>:
  400590:	ff 25 82 0a 20 00    	jmpq   *0x200a82(%rip)        # 601018 <_GLOBAL_OFFSET_TABLE_+0x18>
  400596:	68 00 00 00 00       	pushq  $0x0
  40059b:	e9 e0 ff ff ff       	jmpq   400580 <_init+0x20>

00000000004005a0 <puts@plt>:
  4005a0:	ff 25 7a 0a 20 00    	jmpq   *0x200a7a(%rip)        # 601020 <_GLOBAL_OFFSET_TABLE_+0x20>
  4005a6:	68 01 00 00 00       	pushq  $0x1
  4005ab:	e9 d0 ff ff ff       	jmpq   400580 <_init+0x20>

00000000004005b0 <strlen@plt>:
  4005b0:	ff 25 72 0a 20 00    	jmpq   *0x200a72(%rip)        # 601028 <_GLOBAL_OFFSET_TABLE_+0x28>
  4005b6:	68 02 00 00 00       	pushq  $0x2
  4005bb:	e9 c0 ff ff ff       	jmpq   400580 <_init+0x20>

00000000004005c0 <__stack_chk_fail@plt>:
  4005c0:	ff 25 6a 0a 20 00    	jmpq   *0x200a6a(%rip)        # 601030 <_GLOBAL_OFFSET_TABLE_+0x30>
  4005c6:	68 03 00 00 00       	pushq  $0x3
  4005cb:	e9 b0 ff ff ff       	jmpq   400580 <_init+0x20>

00000000004005d0 <printf@plt>:
  4005d0:	ff 25 62 0a 20 00    	jmpq   *0x200a62(%rip)        # 601038 <_GLOBAL_OFFSET_TABLE_+0x38>
  4005d6:	68 04 00 00 00       	pushq  $0x4
  4005db:	e9 a0 ff ff ff       	jmpq   400580 <_init+0x20>

00000000004005e0 <__libc_start_main@plt>:
  4005e0:	ff 25 5a 0a 20 00    	jmpq   *0x200a5a(%rip)        # 601040 <_GLOBAL_OFFSET_TABLE_+0x40>
  4005e6:	68 05 00 00 00       	pushq  $0x5
  4005eb:	e9 90 ff ff ff       	jmpq   400580 <_init+0x20>

00000000004005f0 <fgets@plt>:
  4005f0:	ff 25 52 0a 20 00    	jmpq   *0x200a52(%rip)        # 601048 <_GLOBAL_OFFSET_TABLE_+0x48>
  4005f6:	68 06 00 00 00       	pushq  $0x6
  4005fb:	e9 80 ff ff ff       	jmpq   400580 <_init+0x20>

0000000000400600 <__gmon_start__@plt>:
  400600:	ff 25 4a 0a 20 00    	jmpq   *0x200a4a(%rip)        # 601050 <_GLOBAL_OFFSET_TABLE_+0x50>
  400606:	68 07 00 00 00       	pushq  $0x7
  40060b:	e9 70 ff ff ff       	jmpq   400580 <_init+0x20>

Disassembly of section .text:

0000000000400610 <_start>:
  400610:	31 ed                	xor    %ebp,%ebp
  400612:	49 89 d1             	mov    %rdx,%r9
  400615:	5e                   	pop    %rsi
  400616:	48 89 e2             	mov    %rsp,%rdx
  400619:	48 83 e4 f0          	and    $0xfffffffffffffff0,%rsp
  40061d:	50                   	push   %rax
  40061e:	54                   	push   %rsp
  40061f:	49 c7 c0 90 08 40 00 	mov    $0x400890,%r8
  400626:	48 c7 c1 20 08 40 00 	mov    $0x400820,%rcx
  40062d:	48 c7 c7 7b 07 40 00 	mov    $0x40077b,%rdi
  400634:	e8 a7 ff ff ff       	callq  4005e0 <__libc_start_main@plt>
  400639:	f4                   	hlt    
  40063a:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)

0000000000400640 <deregister_tm_clones>:
  400640:	b8 6f 10 60 00       	mov    $0x60106f,%eax
  400645:	55                   	push   %rbp
  400646:	48 2d 68 10 60 00    	sub    $0x601068,%rax
  40064c:	48 83 f8 0e          	cmp    $0xe,%rax
  400650:	48 89 e5             	mov    %rsp,%rbp
  400653:	76 1b                	jbe    400670 <deregister_tm_clones+0x30>
  400655:	b8 00 00 00 00       	mov    $0x0,%eax
  40065a:	48 85 c0             	test   %rax,%rax
  40065d:	74 11                	je     400670 <deregister_tm_clones+0x30>
  40065f:	5d                   	pop    %rbp
  400660:	bf 68 10 60 00       	mov    $0x601068,%edi
  400665:	ff e0                	jmpq   *%rax
  400667:	66 0f 1f 84 00 00 00 	nopw   0x0(%rax,%rax,1)
  40066e:	00 00 
  400670:	5d                   	pop    %rbp
  400671:	c3                   	retq   
  400672:	66 66 66 66 66 2e 0f 	data16 data16 data16 data16 nopw %cs:0x0(%rax,%rax,1)
  400679:	1f 84 00 00 00 00 00 

0000000000400680 <register_tm_clones>:
  400680:	be 68 10 60 00       	mov    $0x601068,%esi
  400685:	55                   	push   %rbp
  400686:	48 81 ee 68 10 60 00 	sub    $0x601068,%rsi
  40068d:	48 c1 fe 03          	sar    $0x3,%rsi
  400691:	48 89 e5             	mov    %rsp,%rbp
  400694:	48 89 f0             	mov    %rsi,%rax
  400697:	48 c1 e8 3f          	shr    $0x3f,%rax
  40069b:	48 01 c6             	add    %rax,%rsi
  40069e:	48 d1 fe             	sar    %rsi
  4006a1:	74 15                	je     4006b8 <register_tm_clones+0x38>
  4006a3:	b8 00 00 00 00       	mov    $0x0,%eax
  4006a8:	48 85 c0             	test   %rax,%rax
  4006ab:	74 0b                	je     4006b8 <register_tm_clones+0x38>
  4006ad:	5d                   	pop    %rbp
  4006ae:	bf 68 10 60 00       	mov    $0x601068,%edi
  4006b3:	ff e0                	jmpq   *%rax
  4006b5:	0f 1f 00             	nopl   (%rax)
  4006b8:	5d                   	pop    %rbp
  4006b9:	c3                   	retq   
  4006ba:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)

00000000004006c0 <__do_global_dtors_aux>:
  4006c0:	80 3d a9 09 20 00 00 	cmpb   $0x0,0x2009a9(%rip)        # 601070 <completed.7259>
  4006c7:	75 11                	jne    4006da <__do_global_dtors_aux+0x1a>
  4006c9:	55                   	push   %rbp
  4006ca:	48 89 e5             	mov    %rsp,%rbp
  4006cd:	e8 6e ff ff ff       	callq  400640 <deregister_tm_clones>
  4006d2:	5d                   	pop    %rbp
  4006d3:	c6 05 96 09 20 00 01 	movb   $0x1,0x200996(%rip)        # 601070 <completed.7259>
  4006da:	f3 c3                	repz retq 
  4006dc:	0f 1f 40 00          	nopl   0x0(%rax)

00000000004006e0 <frame_dummy>:
  4006e0:	bf 20 0e 60 00       	mov    $0x600e20,%edi
  4006e5:	48 83 3f 00          	cmpq   $0x0,(%rdi)
  4006e9:	75 05                	jne    4006f0 <frame_dummy+0x10>
  4006eb:	eb 93                	jmp    400680 <register_tm_clones>
  4006ed:	0f 1f 00             	nopl   (%rax)
  4006f0:	b8 00 00 00 00       	mov    $0x0,%eax
  4006f5:	48 85 c0             	test   %rax,%rax
  4006f8:	74 f1                	je     4006eb <frame_dummy+0xb>
  4006fa:	55                   	push   %rbp
  4006fb:	48 89 e5             	mov    %rsp,%rbp
  4006fe:	ff d0                	callq  *%rax
  400700:	5d                   	pop    %rbp
  400701:	e9 7a ff ff ff       	jmpq   400680 <register_tm_clones>

0000000000400706 <verified_pass>:
  400706:	55                   	push   %rbp
  400707:	48 89 e5             	mov    %rsp,%rbp
  40070a:	48 83 ec 30          	sub    $0x30,%rsp
  40070e:	48 89 7d d8          	mov    %rdi,-0x28(%rbp)
  400712:	64 48 8b 04 25 28 00 	mov    %fs:0x28,%rax
  400719:	00 00 
  40071b:	48 89 45 f8          	mov    %rax,-0x8(%rbp)
  40071f:	31 c0                	xor    %eax,%eax
  400721:	48 b8 70 61 73 73 77 	movabs $0x64726f7773736170,%rax
  400728:	6f 72 64 
  40072b:	48 89 45 e0          	mov    %rax,-0x20(%rbp)
  40072f:	c6 45 e8 00          	movb   $0x0,-0x18(%rbp)
  400733:	48 8d 45 e0          	lea    -0x20(%rbp),%rax
  400737:	48 89 c7             	mov    %rax,%rdi
  40073a:	e8 71 fe ff ff       	callq  4005b0 <strlen@plt>
  40073f:	48 89 c2             	mov    %rax,%rdx
  400742:	48 8d 4d e0          	lea    -0x20(%rbp),%rcx
  400746:	48 8b 45 d8          	mov    -0x28(%rbp),%rax
  40074a:	48 89 ce             	mov    %rcx,%rsi
  40074d:	48 89 c7             	mov    %rax,%rdi
  400750:	e8 3b fe ff ff       	callq  400590 <strncmp@plt>
  400755:	85 c0                	test   %eax,%eax
  400757:	75 07                	jne    400760 <verified_pass+0x5a>
  400759:	b8 01 00 00 00       	mov    $0x1,%eax
  40075e:	eb 05                	jmp    400765 <verified_pass+0x5f>
  400760:	b8 00 00 00 00       	mov    $0x0,%eax
  400765:	48 8b 75 f8          	mov    -0x8(%rbp),%rsi
  400769:	64 48 33 34 25 28 00 	xor    %fs:0x28,%rsi
  400770:	00 00 
  400772:	74 05                	je     400779 <verified_pass+0x73>
  400774:	e8 47 fe ff ff       	callq  4005c0 <__stack_chk_fail@plt>
  400779:	c9                   	leaveq 
  40077a:	c3                   	retq   

000000000040077b <main>:
  40077b:	55                   	push   %rbp
  40077c:	48 89 e5             	mov    %rsp,%rbp
  40077f:	48 81 ec 10 08 00 00 	sub    $0x810,%rsp
  400786:	64 48 8b 04 25 28 00 	mov    %fs:0x28,%rax
  40078d:	00 00 
  40078f:	48 89 45 f8          	mov    %rax,-0x8(%rbp)
  400793:	31 c0                	xor    %eax,%eax
  400795:	48 8d 95 f0 f7 ff ff 	lea    -0x810(%rbp),%rdx
  40079c:	b8 00 00 00 00       	mov    $0x0,%eax
  4007a1:	b9 00 01 00 00       	mov    $0x100,%ecx
  4007a6:	48 89 d7             	mov    %rdx,%rdi
  4007a9:	f3 48 ab             	rep stos %rax,%es:(%rdi)
  4007ac:	bf a4 08 40 00       	mov    $0x4008a4,%edi
  4007b1:	b8 00 00 00 00       	mov    $0x0,%eax
  4007b6:	e8 15 fe ff ff       	callq  4005d0 <printf@plt>
  4007bb:	48 8b 15 a6 08 20 00 	mov    0x2008a6(%rip),%rdx        # 601068 <__TMC_END__>
  4007c2:	48 8d 85 f0 f7 ff ff 	lea    -0x810(%rbp),%rax
  4007c9:	be 00 08 00 00       	mov    $0x800,%esi
  4007ce:	48 89 c7             	mov    %rax,%rdi
  4007d1:	e8 1a fe ff ff       	callq  4005f0 <fgets@plt>
  4007d6:	48 8d 85 f0 f7 ff ff 	lea    -0x810(%rbp),%rax
  4007dd:	48 89 c7             	mov    %rax,%rdi
  4007e0:	e8 21 ff ff ff       	callq  400706 <verified_pass>
  4007e5:	85 c0                	test   %eax,%eax
  4007e7:	74 0c                	je     4007f5 <main+0x7a>
  4007e9:	bf bc 08 40 00       	mov    $0x4008bc,%edi
  4007ee:	e8 ad fd ff ff       	callq  4005a0 <puts@plt>
  4007f3:	eb 0a                	jmp    4007ff <main+0x84>
  4007f5:	bf c5 08 40 00       	mov    $0x4008c5,%edi
  4007fa:	e8 a1 fd ff ff       	callq  4005a0 <puts@plt>
  4007ff:	b8 00 00 00 00       	mov    $0x0,%eax
  400804:	48 8b 75 f8          	mov    -0x8(%rbp),%rsi
  400808:	64 48 33 34 25 28 00 	xor    %fs:0x28,%rsi
  40080f:	00 00 
  400811:	74 05                	je     400818 <main+0x9d>
  400813:	e8 a8 fd ff ff       	callq  4005c0 <__stack_chk_fail@plt>
  400818:	c9                   	leaveq 
  400819:	c3                   	retq   
  40081a:	66 0f 1f 44 00 00    	nopw   0x0(%rax,%rax,1)

0000000000400820 <__libc_csu_init>:
  400820:	41 57                	push   %r15
  400822:	41 89 ff             	mov    %edi,%r15d
  400825:	41 56                	push   %r14
  400827:	49 89 f6             	mov    %rsi,%r14
  40082a:	41 55                	push   %r13
  40082c:	49 89 d5             	mov    %rdx,%r13
  40082f:	41 54                	push   %r12
  400831:	4c 8d 25 d8 05 20 00 	lea    0x2005d8(%rip),%r12        # 600e10 <__frame_dummy_init_array_entry>
  400838:	55                   	push   %rbp
  400839:	48 8d 2d d8 05 20 00 	lea    0x2005d8(%rip),%rbp        # 600e18 <__init_array_end>
  400840:	53                   	push   %rbx
  400841:	4c 29 e5             	sub    %r12,%rbp
  400844:	31 db                	xor    %ebx,%ebx
  400846:	48 c1 fd 03          	sar    $0x3,%rbp
  40084a:	48 83 ec 08          	sub    $0x8,%rsp
  40084e:	e8 0d fd ff ff       	callq  400560 <_init>
  400853:	48 85 ed             	test   %rbp,%rbp
  400856:	74 1e                	je     400876 <__libc_csu_init+0x56>
  400858:	0f 1f 84 00 00 00 00 	nopl   0x0(%rax,%rax,1)
  40085f:	00 
  400860:	4c 89 ea             	mov    %r13,%rdx
  400863:	4c 89 f6             	mov    %r14,%rsi
  400866:	44 89 ff             	mov    %r15d,%edi
  400869:	41 ff 14 dc          	callq  *(%r12,%rbx,8)
  40086d:	48 83 c3 01          	add    $0x1,%rbx
  400871:	48 39 eb             	cmp    %rbp,%rbx
  400874:	75 ea                	jne    400860 <__libc_csu_init+0x40>
  400876:	48 83 c4 08          	add    $0x8,%rsp
  40087a:	5b                   	pop    %rbx
  40087b:	5d                   	pop    %rbp
  40087c:	41 5c                	pop    %r12
  40087e:	41 5d                	pop    %r13
  400880:	41 5e                	pop    %r14
  400882:	41 5f                	pop    %r15
  400884:	c3                   	retq   
  400885:	66 66 2e 0f 1f 84 00 	data16 nopw %cs:0x0(%rax,%rax,1)
  40088c:	00 00 00 00 

0000000000400890 <__libc_csu_fini>:
  400890:	f3 c3                	repz retq 

Disassembly of section .fini:

0000000000400894 <_fini>:
  400894:	48 83 ec 08          	sub    $0x8,%rsp
  400898:	48 83 c4 08          	add    $0x8,%rsp
  40089c:	c3                   	retq   
