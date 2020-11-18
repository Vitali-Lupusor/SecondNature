"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const createUsersJob_1 = __importDefault(require("./createUsersJob"));
const createMessagesJob_1 = __importDefault(require("./createMessagesJob"));
const createInvoicesJob_1 = __importDefault(require("./createInvoicesJob"));
const jobs = {
    createUsersJob: createUsersJob_1.default,
    createMessagesJob: createMessagesJob_1.default,
    createInvoicesJob: createInvoicesJob_1.default,
};
exports.default = jobs;
//# sourceMappingURL=index.js.map