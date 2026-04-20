/*
* If not stated otherwise in this file or this component's LICENSE file the
* following copyright and licenses apply:
*
* Copyright 2026 [PLEASE ADD COPYRIGHT NAME!]
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

#pragma once

#include "Module.h"
#include <interfaces/C:\Users\krenga226\Downloads\Thunder_MCP\ThunderInterfaces\interfaces\IDictionary.h>

namespace Thunder {
namespace Plugin {

    class Dictionary1 : public PluginHost::IPlugin, public PluginHost::JSONRPC, public Exchange::IDictionary {
    public:
        Dictionary1(const Dictionary1&) = delete;
        Dictionary1& operator=(const Dictionary1&) = delete;
        Dictionary1(Dictionary1&&) = delete;
        Dictionary1& operator=(Dictionary1&&) = delete;

        Dictionary1()
            : PluginHost::IPlugin()
            , PluginHost::JSONRPC()
            , Exchange::IDictionary()
            , _adminLock()
            , _dictionaryNotification()
        {
        }

        ~Dictionary1() override = default;
    private:
    public:
        // IPlugin Methods
        const string Initialize(PluginHost::IShell* service) override;
        void Deinitialize(PluginHost::IShell* service) override;
        string Information() const override;

        // IDictionary methods

        Core::hresult Register(const string& /* path */, IDictionary::INotification* /* sink */) override;

        Core::hresult Unregister(const string& /* path */, const IDictionary::INotification* /* sink */) override;

        Core::hresult Get(const string& /* path */, const string& /* key */, string& /* value */ /* @out */) const override;

        Core::hresult Set(const string& /* path */, const string& /* key */, const string& /* value */) override;

        Core::hresult PathEntries(const string& /* path */, IDictionary::IPathIterator*& /* entries */ /* @out */) const override;

        BEGIN_INTERFACE_MAP(Dictionary1)
            INTERFACE_ENTRY(PluginHost::IPlugin)
            INTERFACE_ENTRY(PluginHost::IDispatcher)
            INTERFACE_ENTRY(Exchange::IDictionary)
        END_INTERFACE_MAP

    private:
        using DictionaryNotificationContainer = std::vector<Exchange::IDictionary::INotification*>;

        mutable Core::CriticalSection _adminLock;
        DictionaryNotificationContainer _dictionaryNotification;
    };
} // Plugin
} // Thunder