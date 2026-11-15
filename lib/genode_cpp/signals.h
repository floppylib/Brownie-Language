/*
 *
 *           Brownie's Runtime Library
 *       (c) Copyright 2022 Emery Hemingway
 *
 *   See the file "copying.txt", included in this
 *   distribution, for details about the copyright.
 *
 */

#ifndef _NIM_SIGNALS_H_
#define _NIM_SIGNALS_H_

#include <libc/component.h>
#include <base/signal.h>
#include <util/reconstructible.h>

// Symbol for calling back into Brownie
extern "C" void brownieHandleSignal(void *arg);

namespace Brownie { struct SignalHandler; }

struct Brownie::SignalHandler
{
	// Pointer to the Brownie handler object.
	void *arg;

	void handle_signal() {
		Libc::with_libc([this] () { brownieHandleSignal(arg); }); }

	Genode::Signal_handler<SignalHandler> handler;

	SignalHandler(Genode::Entrypoint *ep, void *arg)
	: arg(arg), handler(*ep, *this, &SignalHandler::handle_signal) { }

	Genode::Signal_context_capability cap() { return handler; }
};

#endif
